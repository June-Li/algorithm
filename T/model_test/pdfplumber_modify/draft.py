    pages = pdf.pages
    for index in range(2):
        bbox = pages[index].bbox
        print("page bbox", bbox)
        print("page rects", len(pages[index].rects))
        print("page rect_edges", len(pages[index].rect_edges))
        print("page chars", len(pages[index].chars))
        print("page edges", len(pages[index].edges))
        print("page lines", len(pages[index].lines))
        print("page tables", len(pages[index].extract_tables()))
          