#!/usr/bin/env python3
import os
import sys
import argparse
import base64
from google import genai

IMAGE_DIR = os.environ.get("GEMINI_IMAGE_DIR", os.getcwd())   # default save folder for generated images

def main():
    parser = argparse.ArgumentParser(description="Gemini API CLI Wrapper for Claude Code")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Text Generation Command
    gen_parser = subparsers.add_parser("generate", help="Generate text using Gemini")
    gen_parser.add_argument("--model", default="gemini-3.1-pro-preview", help="Gemini model to use")
    gen_parser.add_argument("--prompt", required=True, help="Prompt text")

    # Multimodal Vision Command
    vis_parser = subparsers.add_parser("vision", help="Analyze files using Gemini")
    vis_parser.add_argument("--model", default="gemini-3.1-pro-preview", help="Gemini model to use")
    vis_parser.add_argument("--file", required=True, help="Path to the local file")
    vis_parser.add_argument("--prompt", required=True, help="Prompt text")

    # Image Generation Command
    img_parser = subparsers.add_parser("image", help="Generate an image and save it to a file")
    img_parser.add_argument("--model", default="gemini-nano-banana-2.1", help="Gemini image model to use")
    img_parser.add_argument("--prompt", required=True, help="Prompt text")
    img_parser.add_argument("--out", default="generated_image.jpg", help="Output path; a bare filename goes to GEMINI_IMAGE_DIR (default: current folder); always saved as .jpg")
    img_parser.add_argument("--aspect", default="1:1", help='Aspect ratio, e.g. 1:1, 16:9, 9:16')
    img_parser.add_argument("--size", default="1K", help="Image size, e.g. 1K, 2K")

    args = parser.parse_args()

    # The genai SDK automatically detects the GEMINI_API_KEY environment variable.
    # We explicitly check here to provide a clear error message for Claude Code.
    if not os.environ.get("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    client = genai.Client()

    try:
        if args.command == "generate":
            response = client.models.generate_content(
                model=args.model,
                contents=args.prompt
            )
            print(response.text)

        elif args.command == "vision":
            if not os.path.exists(args.file):
                print(f"Error: File not found at {args.file}", file=sys.stderr)
                sys.exit(1)
            
            # Upload the asset to Google's File API temporarily for processing
            uploaded_file = client.files.upload(file=args.file)
            
            response = client.models.generate_content(
                model=args.model,
                contents=[uploaded_file, args.prompt]
            )
            print(response.text)
            
            # Cleanup the file from the API to maintain hygiene
            client.files.delete(name=uploaded_file.name)

        elif args.command == "image":
            out = os.path.splitext(args.out)[0] + ".jpg"   # the API only returns JPEG
            if not os.path.dirname(out):
                out = os.path.join(IMAGE_DIR, out)
            interaction = client.interactions.create(
                model=args.model,
                input=args.prompt,
                response_format={"type": "image", "mime_type": "image/jpeg",
                                 "aspect_ratio": args.aspect, "image_size": args.size},
            )
            image = interaction.output_image
            if not image:
                print("Error: the model returned no image.", file=sys.stderr)
                sys.exit(1)
            with open(out, "wb") as f:
                f.write(base64.b64decode(image.data))
            print(f"Image saved as {os.path.abspath(out)}")

    except Exception as e:
        print(f"API Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()