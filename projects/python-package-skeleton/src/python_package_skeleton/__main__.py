from . import hello
import argparse

def main() -> None:
    p = argparse.ArgumentParser(description="Skeleton greeter")
    p.add_argument("--name", default="World")
    args = p.parse_args()
    print(hello(args.name))

if __name__ == "__main__":
    main()
