from textnode import TextType, TextNode

def main():
    test = TextNode("This is some anchor text", TextType.LINK, "https://www.wp.pl")
    print(test)

if __name__ == "__main__":
    main()