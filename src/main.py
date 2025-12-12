import clipboard

if __name__ == "__main__":
    try:
        clipboard.main()
    except (KeyboardInterrupt):
        print("> Finalizando script...")