"""Chuyển Markdown (có công thức LaTeX) sang DOCX với định dạng báo cáo.

Cách dùng:
    python scripts/md_to_docx.py docs/proposal/proposal_final.md \
        docs/proposal/proposal_final.docx

Đặc điểm:
    * Công thức $$...$$ và \\(...\\) được pandoc chuyển thành equation gốc của
      Word (OMML), không phải ảnh nên vẫn sửa được trong Word.
    * Khổ A4, lề chuẩn, font Times New Roman 13pt, giãn dòng 1.15.
    * Bảng có kẻ khung, dòng tiêu đề in đậm và lặp lại khi sang trang.
    * Footer có số trang.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pypandoc
from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

BODY_FONT = "Times New Roman"
CODE_FONT = "Consolas"
BODY_SIZE = 13
CODE_SIZE = 10
TABLE_SIZE = 12

# (cỡ chữ, đậm, nghiêng, space_before, space_after)
HEADING_FORMATS = {
    "Heading 1": (16, True, False, 18, 8),
    "Heading 2": (14, True, False, 14, 6),
    "Heading 3": (13, True, False, 12, 6),
    "Heading 4": (13, True, True, 10, 4),
    "Heading 5": (13, False, True, 10, 4),
}

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
M = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"

# Thứ tự phần tử bắt buộc của OOXML (ISO/IEC 29500). Word rất nghiêm: chỉ cần
# sai thứ tự một phần tử là Word báo "unreadable content", tự sửa file và có
# thể làm mất công thức/bảng. LibreOffice thì bỏ qua nên không phát hiện được.
RPR_ORDER = [
    "rStyle",
    "rFonts",
    "b",
    "bCs",
    "i",
    "iCs",
    "caps",
    "smallCaps",
    "strike",
    "dstrike",
    "outline",
    "shadow",
    "emboss",
    "imprint",
    "noProof",
    "snapToGrid",
    "vanish",
    "webHidden",
    "color",
    "spacing",
    "w",
    "kern",
    "position",
    "sz",
    "szCs",
    "highlight",
    "u",
    "effect",
    "bdr",
    "shd",
    "fitText",
    "vertAlign",
    "rtl",
    "cs",
    "em",
    "lang",
    "eastAsianLayout",
    "specVanish",
    "oMath",
    "rPrChange",
]
PPR_ORDER = [
    "pStyle",
    "keepNext",
    "keepLines",
    "pageBreakBefore",
    "framePr",
    "widowControl",
    "numPr",
    "suppressLineNumbers",
    "pBdr",
    "shd",
    "tabs",
    "suppressAutoHyphens",
    "kinsoku",
    "wordWrap",
    "overflowPunct",
    "topLinePunct",
    "autoSpaceDE",
    "autoSpaceDN",
    "bidi",
    "adjustRightInd",
    "snapToGrid",
    "spacing",
    "ind",
    "contextualSpacing",
    "mirrorIndents",
    "suppressOverlap",
    "jc",
    "textDirection",
    "textAlignment",
    "textboxTightWrap",
    "outlineLvl",
    "divId",
    "cnfStyle",
    "rPr",
    "sectPr",
    "pPrChange",
]
TBLPR_ORDER = [
    "tblStyle",
    "tblpPr",
    "tblOverlap",
    "bidiVisual",
    "tblStyleRowBandSize",
    "tblStyleColBandSize",
    "tblW",
    "jc",
    "tblCellSpacing",
    "tblInd",
    "tblBorders",
    "shd",
    "tblLayout",
    "tblCellMar",
    "tblLook",
    "tblCaption",
    "tblDescription",
    "tblPrChange",
]
TRPR_ORDER = [
    "cnfStyle",
    "divId",
    "gridBefore",
    "gridAfter",
    "wBefore",
    "wAfter",
    "cantSplit",
    "trHeight",
    "tblHeader",
    "tblCellSpacing",
    "jc",
    "hidden",
    "ins",
    "del",
    "trPrChange",
]
SETTINGS_ORDER = [
    "writeProtection",
    "view",
    "zoom",
    "removePersonalInformation",
    "removeDateAndTime",
    "doNotDisplayPageBoundaries",
    "displayBackgroundShape",
    "printPostScriptOverText",
    "printFractionalCharacterWidth",
    "printFormsData",
    "embedTrueTypeFonts",
    "embedSystemFonts",
    "saveSubsetFonts",
    "saveFormsData",
    "mirrorMargins",
    "alignBordersAndEdges",
    "bordersDoNotSurroundHeader",
    "bordersDoNotSurroundFooter",
    "gutterAtTop",
    "hideSpellingErrors",
    "hideGrammaticalErrors",
    "activeWritingStyle",
    "proofState",
    "formsDesign",
    "attachedTemplate",
    "linkStyles",
    "stylePaneFormatFilter",
    "stylePaneSortMethod",
    "documentType",
    "mailMerge",
    "revisionView",
    "trackChanges",
    "doNotTrackMoves",
    "doNotTrackFormatting",
    "documentProtection",
    "autoFormatOverride",
    "styleLockTheme",
    "styleLockQFSet",
    "defaultTabStop",
    "autoHyphenation",
    "consecutiveHyphenLimit",
    "hyphenationZone",
    "doNotHyphenateCaps",
    "showEnvelope",
    "summaryLength",
    "clickAndTypeStyle",
    "defaultTableStyle",
    "evenAndOddHeaders",
    "bookFoldRevPrinting",
    "bookFoldPrinting",
    "bookFoldPrintingSheets",
    "drawingGridHorizontalSpacing",
    "drawingGridVerticalSpacing",
    "displayHorizontalDrawingGridEvery",
    "displayVerticalDrawingGridEvery",
    "doNotUseMarginsForDrawingGridOrigin",
    "drawingGridHorizontalOrigin",
    "drawingGridVerticalOrigin",
    "doNotShadeFormData",
    "noPunctuationKerning",
    "characterSpacingControl",
    "printTwoOnOne",
    "strictFirstAndLastChars",
    "noLineBreaksAfter",
    "noLineBreaksBefore",
    "savePreviewPicture",
    "doNotValidateAgainstSchema",
    "saveInvalidXml",
    "ignoreMixedContent",
    "alwaysShowPlaceholderText",
    "doNotDemarcateInvalidXml",
    "saveXmlDataOnly",
    "useXSLTWhenSaving",
    "saveThroughXslt",
    "showXMLTags",
    "alwaysMergeEmptyNamespace",
    "updateFields",
    "hdrShapeDefaults",
    "footnotePr",
    "endnotePr",
    "compat",
    "docVars",
    "rsids",
    "mathPr",
    "uiCompat97To2003",
    "attachedSchema",
    "themeFontLang",
    "clrSchemeMapping",
    "doNotIncludeSubdocsInStats",
    "doNotAutoCompressPictures",
    "forceUpgrade",
    "captions",
    "readModeInkLockDown",
    "smartTagType",
    "schemaLibrary",
    "shapeDefaults",
    "doNotEmbedSmartTags",
    "decimalSymbol",
    "listSeparator",
]


def _localname(element) -> str:
    return element.tag.split("}")[-1]


def _insert_ordered(parent, element, order: list[str]) -> None:
    """Chèn element vào parent đúng thứ tự schema OOXML."""
    rank = order.index(_localname(element))
    for child in parent:
        name = _localname(child)
        if name in order and order.index(name) > rank:
            child.addprevious(element)
            return
    parent.append(element)


def _set_run_font(rpr, name: str) -> None:
    """Gán font cho cả ascii, hAnsi, cs và eastAsia (cần cho tiếng Việt)."""
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        _insert_ordered(rpr, rfonts, RPR_ORDER)  # rFonts phải đứng đầu rPr
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), name)


def _ensure_code_style(doc) -> None:
    """Tạo style 'Source Code' nếu reference.docx chưa có.

    pandoc tự thêm style này khi ghi file, nhưng chỉ khi nó chưa tồn tại;
    nếu ta định nghĩa sẵn thì mọi thiết lập dưới đây được giữ nguyên.
    Quan trọng: wordWrap=off để sơ đồ ASCII không bị ngắt dòng.
    """
    names = {style.name for style in doc.styles}
    if "Source Code" in names:
        style = doc.styles["Source Code"]
    else:
        style = doc.styles.add_style("Source Code", WD_STYLE_TYPE.PARAGRAPH)
    style.base_style = doc.styles["Normal"]
    style.next_paragraph_style = doc.styles["Normal"]
    # Không canh đều: sơ đồ ASCII cần khoảng trắng đúng 1 ký tự.
    fmt = style.paragraph_format
    fmt.alignment = WD_ALIGN_PARAGRAPH.LEFT
    fmt.space_before = Pt(4)
    fmt.space_after = Pt(4)
    fmt.line_spacing_rule = WD_LINE_SPACING.SINGLE

    ppr = style.element.get_or_add_pPr()
    word_wrap = OxmlElement("w:wordWrap")
    word_wrap.set(qn("w:val"), "off")
    _insert_ordered(ppr, word_wrap, PPR_ORDER)  # phải đứng trước spacing/jc


def build_reference_docx(path: Path) -> None:
    """Tạo file mẫu (reference.docx) từ mặc định của pandoc rồi chỉnh style."""
    pandoc = pypandoc.get_pandoc_path()
    data = subprocess.run(
        [pandoc, "--print-default-data-file", "reference.docx"],
        capture_output=True,
        check=True,
    ).stdout
    path.write_bytes(data)

    doc = Document(str(path))

    # --- Khổ giấy A4 và lề ---
    for section in doc.sections:
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin = Cm(3.0)
        section.right_margin = Cm(2.0)
        # w:header, w:footer, w:gutter là thuộc tính bắt buộc của w:pgMar;
        # thiếu chúng thì Word coi file sai chuẩn.
        section.header_distance = Cm(1.25)
        section.footer_distance = Cm(1.25)
        section.gutter = Cm(0)

    # --- Font mặc định cho mọi style đoạn văn ---
    for style in doc.styles:
        if style.type == WD_STYLE_TYPE.PARAGRAPH:
            style.font.name = BODY_FONT
            size = style.font.size or Pt(BODY_SIZE)
            style.font.size = size
            _set_run_font(style.element.get_or_add_rPr(), BODY_FONT)
        elif style.type == WD_STYLE_TYPE.CHARACTER:
            _set_run_font(style.element.get_or_add_rPr(), BODY_FONT)

    def para_style(name: str):
        try:
            return doc.styles[name]
        except KeyError:
            return None

    # --- Văn bản thường: canh đều hai bên, giãn dòng 1.15 ---
    for name in ("Normal", "Body Text", "First Paragraph", "Compact"):
        style = para_style(name)
        if style is None:
            continue
        style.font.size = Pt(BODY_SIZE)
        fmt = style.paragraph_format
        fmt.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        fmt.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        fmt.line_spacing = 1.15
        fmt.space_after = Pt(6)
        fmt.space_before = Pt(0)

    # --- Tiêu đề phân cấp ---
    for name, (size, bold, italic, before, after) in HEADING_FORMATS.items():
        style = para_style(name)
        if style is None:
            continue
        style.font.size = Pt(size)
        style.font.bold = bold
        style.font.italic = italic
        style.font.color.rgb = RGBColor(0, 0, 0)
        _set_run_font(style.element.get_or_add_rPr(), BODY_FONT)
        fmt = style.paragraph_format
        fmt.alignment = WD_ALIGN_PARAGRAPH.LEFT
        fmt.space_before = Pt(before)
        fmt.space_after = Pt(after)
        fmt.keep_with_next = True
        fmt.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        fmt.line_spacing = 1.15

    # --- Trích dẫn (blockquote) ---
    style = para_style("Block Text")
    if style is not None:
        style.font.size = Pt(BODY_SIZE)
        style.font.italic = True
        style.paragraph_format.left_indent = Cm(1.0)
        style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # --- Khối mã / sơ đồ ASCII: font đều, cỡ nhỏ để không tràn dòng ---
    _ensure_code_style(doc)
    for name, size in (("Source Code", CODE_SIZE), ("Verbatim Char", CODE_SIZE)):
        style = para_style(name)
        if style is None:
            continue
        style.font.size = Pt(size)
        style.font.name = CODE_FONT
        _set_run_font(style.element.get_or_add_rPr(), CODE_FONT)
        if style.type == WD_STYLE_TYPE.PARAGRAPH:
            style.paragraph_format.space_after = Pt(0)
            style.paragraph_format.space_before = Pt(0)
            style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
            # Không canh đều: sơ đồ ASCII cần khoảng trắng đúng 1 ký tự.
            style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

    # --- Chú thích, caption ---
    for name in ("Footnote Text", "Table Caption", "Image Caption", "Caption"):
        style = para_style(name)
        if style is not None:
            style.font.size = Pt(11)

    doc.save(str(path))


def _set_table_borders(table) -> None:
    tbl_pr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        element = OxmlElement(f"w:{edge}")
        element.set(qn("w:val"), "single")
        element.set(qn("w:sz"), "4")
        element.set(qn("w:space"), "0")
        element.set(qn("w:color"), "000000")
        borders.append(element)
    # tblBorders phải đứng trước tblLayout/tblLook, nếu không Word sẽ báo lỗi file.
    _insert_ordered(tbl_pr, borders, TBLPR_ORDER)


def _repeat_header_row(row) -> None:
    tr_pr = row._tr.get_or_add_trPr()
    header = OxmlElement("w:tblHeader")
    header.set(qn("w:val"), "true")
    _insert_ordered(tr_pr, header, TRPR_ORDER)


def _fix_pandoc_math(doc) -> tuple[int, int]:
    """Sửa hai lỗi OMML do pandoc 3.9 sinh ra khiến Word coi file là hỏng.

    1. pandoc ghi <m:mcPr><m:mcJc/><m:count/></m:mcPr>, nhưng schema OOXML bắt
       buộc <m:count/> đứng trước <m:mcJc/>.
    2. pandoc ghi <m:rPr><m:nor/><m:sty/></m:rPr> cho chữ thường trong công
       thức (\\text{...}); schema chỉ cho phép một trong hai.

    Trả về (số chỗ sửa thứ tự, số chỗ bỏ m:sty trùng).
    """
    reordered = 0
    for mc_pr in doc.element.iter(f"{M}mcPr"):
        count = mc_pr.find(f"{M}count")
        mc_jc = mc_pr.find(f"{M}mcJc")
        if count is not None and mc_jc is not None:
            if list(mc_pr).index(count) > list(mc_pr).index(mc_jc):
                mc_jc.addprevious(count)
                reordered += 1

    # m:nor (chữ thường) đã bao hàm ý nghĩa của m:sty m:val="p"; giữ m:nor để
    # chữ trong công thức dùng đúng font văn bản (Times New Roman).
    deduped = 0
    for r_pr in doc.element.iter(f"{M}rPr"):
        nor = r_pr.find(f"{M}nor")
        sty = r_pr.find(f"{M}sty")
        if nor is not None and sty is not None:
            r_pr.remove(sty)
            deduped += 1
    return reordered, deduped


def _add_page_number(paragraph) -> None:
    """Chèn trường PAGE theo dạng chuẩn Word (5 run), để Word web và Word
    trên Windows đều đọc được và tự cập nhật số trang."""

    def _new_run():
        run = paragraph.add_run()
        run.font.size = Pt(11)
        run.font.name = BODY_FONT
        _set_run_font(run._r.get_or_add_rPr(), BODY_FONT)
        return run

    def _field(kind: str):
        run = _new_run()
        element = OxmlElement("w:fldChar")
        element.set(qn("w:fldCharType"), kind)
        run._r.append(element)

    _field("begin")
    instr_run = _new_run()
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    instr_run._r.append(instr)
    _field("separate")
    _new_run().add_text("1")  # giá trị tạm, Word sẽ tự cập nhật
    _field("end")


def _enable_update_fields(doc) -> None:
    """Yêu cầu Word cập nhật lại trường (số trang) khi mở file."""
    settings = doc.settings.element
    if settings.find(qn("w:updateFields")) is not None:
        return
    element = OxmlElement("w:updateFields")
    element.set(qn("w:val"), "true")
    _insert_ordered(settings, element, SETTINGS_ORDER)


def _check_element_order(root, label: str) -> list[str]:
    """Tự kiểm tra thứ tự phần tử XML; trả về danh sách lỗi tìm được."""
    checks = {
        "rPr": RPR_ORDER,
        "pPr": PPR_ORDER,
        "tblPr": TBLPR_ORDER,
        "trPr": TRPR_ORDER,
        "mcPr": ["count", "mcJc"],
    }
    problems = []
    for tag, order in checks.items():
        for element in root.iter(f"{{{W[1:]}}}{tag}" if tag != "mcPr" else f"{M}{tag}"):
            seq = [
                _localname(child)
                for child in element
                if child.tag.startswith(W) or child.tag.startswith(M)
            ]
            ranks = [order.index(name) for name in seq if name in order]
            if ranks != sorted(ranks):
                problems.append(f"{label}: <{tag}> sai thứ tự {seq}")

    # m:rPr của công thức: chỉ được có lit / (nor hoặc scr+sty) / brk / aln,
    # và m:nor không được đi cùng m:scr hay m:sty.
    math_rpr = ["lit", "nor", "scr", "sty", "brk", "aln"]
    for element in root.iter(f"{M}rPr"):
        seq = [_localname(child) for child in element]
        unknown = [name for name in seq if name not in math_rpr]
        ranks = [math_rpr.index(name) for name in seq if name in math_rpr]
        if unknown or ranks != sorted(ranks):
            problems.append(f"{label}: <m:rPr> không hợp lệ {seq}")
        if "nor" in seq and ("scr" in seq or "sty" in seq):
            problems.append(f"{label}: <m:rPr> có m:nor đi cùng m:scr/m:sty {seq}")
    # pPr/rPr/tcPr phải là phần tử đầu của đoạn/run/ô
    for parent in root.iter(f"{W}p"):
        children = list(parent)
        if (
            children
            and _localname(children[0]) != "pPr"
            and any(_localname(c) == "pPr" for c in children)
        ):
            problems.append(f"{label}: <w:p> có pPr không ở đầu")
    for parent in root.iter(f"{W}r"):
        children = list(parent)
        if (
            any(_localname(c) == "rPr" for c in children)
            and _localname(children[0]) != "rPr"
        ):
            problems.append(f"{label}: <w:r> có rPr không ở đầu")
    return problems


def _has_manual_line_break(paragraph) -> bool:
    """Đoạn có ngắt dòng thủ công (w:br), ví dụ các dòng mục lục."""
    return bool(paragraph._p.findall(f".//{qn('w:br')}"))


def postprocess(path: Path) -> tuple[int, int]:
    """Chỉnh bảng, sửa công thức, thêm số trang; trả về (số bảng, số đoạn)."""
    doc = Document(str(path))

    # Sửa các lỗi OMML do pandoc sinh ra (nếu có).
    math_reordered, math_deduped = _fix_pandoc_math(doc)

    # Canh đều chỉ hợp lý cho đoạn văn xuôi. Đoạn có ngắt dòng thủ công
    # (mục lục, danh sách dòng) phải canh trái, nếu không Word sẽ giãn
    # khoảng trắng giữa các từ cho đầy dòng.
    for paragraph in doc.paragraphs:
        if not _has_manual_line_break(paragraph):
            continue
        if paragraph.alignment in (None, WD_ALIGN_PARAGRAPH.JUSTIFY):
            paragraph.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

    for table in doc.tables:
        _set_table_borders(table)
        for row_index, row in enumerate(table.rows):
            if row_index == 0:
                _repeat_header_row(row)
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    paragraph.paragraph_format.space_after = Pt(2)
                    paragraph.paragraph_format.space_before = Pt(2)
                    paragraph.paragraph_format.line_spacing = 1.0
                    # Giữ canh lề cột do pandoc sinh ra (số căn phải);
                    # chỉ chặn việc kế thừa justify từ style Normal.
                    if paragraph.alignment is None:
                        paragraph.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    for run in paragraph.runs:
                        run.font.size = Pt(TABLE_SIZE)
                        if row_index == 0:
                            run.font.bold = True

    for section in doc.sections:
        footer = section.footer
        paragraphs = footer.paragraphs
        paragraph = paragraphs[0] if paragraphs else footer.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        _add_page_number(paragraph)

    _enable_update_fields(doc)

    # Tự kiểm tra thứ tự phần tử trước khi ghi file: nếu sai, Word sẽ coi
    # file là hỏng và tự sửa, có thể làm mất công thức.
    problems = _check_element_order(doc.element, "document") + _check_element_order(
        doc.styles.element, "styles"
    )
    if math_reordered or math_deduped:
        print(
            f"   sửa lỗi công thức do pandoc: {math_reordered} chỗ sai thứ tự, "
            f"{math_deduped} chỗ thừa m:sty"
        )
    if problems:
        for p in problems[:5]:
            print(f"   CẢNH BÁO {p}")
    else:
        print("   kiểm tra thứ tự XML: OK")

    doc.save(str(path))
    return len(doc.tables), len(doc.paragraphs)


def convert(md_path: Path, docx_path: Path, ref_path: Path) -> None:
    build_reference_docx(ref_path)
    pypandoc.convert_file(
        str(md_path),
        "docx",
        format=(
            "markdown+tex_math_dollars+tex_math_single_backslash+pipe_tables"
            "+footnotes+raw_tex+hard_line_breaks"
        ),
        outputfile=str(docx_path),
        extra_args=[f"--reference-doc={ref_path}", "--standalone"],
    )
    tables, paragraphs = postprocess(docx_path)
    print(f"OK: {docx_path} ({tables} bảng, {paragraphs} đoạn)")


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__)
        return 2
    md_path = Path(argv[1]).resolve()
    docx_path = Path(argv[2]).resolve()
    if not md_path.is_file():
        print(f"Không tìm thấy: {md_path}")
        return 1
    ref_path = docx_path.with_name("_reference.docx")
    convert(md_path, docx_path, ref_path)
    ref_path.unlink(missing_ok=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
