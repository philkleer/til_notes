#!/usr/bin/env python3
import argparse

def main():
    parser = argparse.ArgumentParser(description="Tiny demo CLI")
    parser.add_argument("--name", default="World", help="Who to greet")
    args = parser.parse_args()
    print(f"Hello, {args.name}!")

if __name__ == "__main__":
    main()
