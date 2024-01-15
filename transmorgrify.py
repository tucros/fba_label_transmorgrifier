from pypdf import PdfReader, PdfWriter, Transformation

LETTER_WIDTH = 612  # 8.5 inches in points
LETTER_HEIGHT = 792  # 11 inches in points

ORIG_WIDTH = 306
ORIG_HEIGHT = 432
SCALED_WIDTH = int(0.95 * ORIG_WIDTH)
WIDTH_DIFF = ORIG_WIDTH - SCALED_WIDTH

LABEL_HEIGHT = 240  # 3.33 inches in points

TOP_MARGIN = 72 / 2  # 1/2 inch margin
SIDE_MARGIN = 72 / 8  # 1/8 inch margin


def extract_pages(source_pdf, target_pdf):
    with open(source_pdf, "rb") as file:
        reader = PdfReader(file)
        writer = PdfWriter()

        new_page = None
        for i in range(len(reader.pages)):
            page = reader.pages[i]

            if i % 6 == 0:
                new_page = writer.add_blank_page(
                    width=LETTER_WIDTH, height=LETTER_HEIGHT
                )

            # Calculate position to insert the half page
            column = 0 if i % 6 < 3 else 1
            x_offset = ((LETTER_WIDTH / 2) * column) + SIDE_MARGIN
            if column == 1:
                x_offset += WIDTH_DIFF
            else:
                x_offset += WIDTH_DIFF / 2

            label_top = (LETTER_HEIGHT - TOP_MARGIN) - (i % 3 * LABEL_HEIGHT)
            y_offset = label_top - ORIG_HEIGHT
            transform = Transformation().translate(x_offset, y_offset).scale(0.95, 1)
            new_page.merge_transformed_page(page, transform)

        # Write the new PDF to a file
        with open(target_pdf, "wb") as output_file:
            writer.write(output_file)


if __name__ == "__main__":
    # Get the input pdf from the command line
    import sys

    if len(sys.argv) != 3:
        print("Usage: python test.py source.pdf target.pdf")
        sys.exit(1)

    source_pdf = sys.argv[1]
    target_pdf = sys.argv[2]
    extract_pages(source_pdf, target_pdf)
