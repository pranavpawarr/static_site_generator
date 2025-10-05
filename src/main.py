from textnode import TextNode,InlineTextType

def main():
    node = TextNode("This is some anchor text", InlineTextType.LINK, "https://www.boot.dev")
    print(node)

if __name__ == "__main__":
    main()