from bulletin.actions import generate_now


def main():
    html_path, pdf_path, _ = generate_now()
    print(f"Готово:\n  HTML: {html_path}\n  PDF:  {pdf_path}")


if __name__ == "__main__":
    main()
