# 📄 Unstructured PDF Element Categories

This document lists and defines the various `Element` categories returned by the [`unstructured`](https://github.com/Unstructured-IO/unstructured) Python library when parsing documents like PDFs using `partition_pdf`.

The `category` field (formerly `type`) provides semantic context for each extracted chunk, making it easier to structure content for downstream use such as LLMs, vector databases, or information extraction.

---

## 📚 Element Categories

| **Category**         | **Description**                                                                 |
|----------------------|----------------------------------------------------------------------------------|
| `Title`              | A document or section title. Often bold or in a large font.                      |
| `NarrativeText`      | Main prose text or paragraphs. Long-form natural language.                       |
| `ListItem`           | Items from bullet lists or numbered lists.                                       |
| `Table`              | Structured tabular data, extracted as a block of text.                           |
| `TableCaption`       | Caption describing a table. Often found above or below tables.                   |
| `FigureCaption`      | Caption describing an image or figure.                                           |
| `SectionHeader`      | Headers or subheaders organizing sections of the document.                       |
| `PageBreak`          | Marks the end of a page. Used to denote logical document boundaries.             |
| `Address`            | A detected street or mailing address.                                            |
| `EmailAddress`       | An email address found in the document.                                          |
| `PhoneNumber`        | A phone number found in the document.                                            |
| `Header`             | Repeating text found at the top of pages (e.g., document name, date).            |
| `Footer`             | Repeating text at the bottom of pages (e.g., page number, copyright).            |
| `Image`              | An inline image or reference to an image within the PDF.                         |
| `TitlePage`          | Special classification for title pages including author, institution, etc.       |
| `UncategorizedText`  | Fallback label when text doesn't fit any known category.                         |
| `Formula`            | Mathematical or scientific equations.                                            |
| `CodeBlock`          | Preformatted code blocks, typically from technical or programming documents.     |
| `Footnote`           | Notes appearing at the bottom of a page.                                         |
| `TitleHeader`        | A header-style title repeated across sections (e.g., report title).              |
| `Reference`          | Bibliography or citation text entries.                                           |

---

## 🔧 Usage Example

```python
from unstructured.partition.pdf import partition_pdf

elements = partition_pdf("document.pdf")

for el in elements:
    print(f"{el.category}: {el.text[:100]}")  # Preview first 100 characters
