# Contributing

Thanks for your interest in VRAM Zero.

## Reporting a bug

Open an issue with the **Bug report** form. Useful details: VRAM Zero version, Windows version, GPU model and driver version, and the output of `nvidia-smi` in a terminal.

## Suggesting an improvement

Open an issue with the **Feature request** form and describe the situation you want to handle.

A frequent request is to add an application to the "local AI" list. Please give the executable name (for example `koboldcpp.exe`) and what the tool does.

## Pull requests

1. Open an issue first for anything larger than a small fix.
2. Fork the repository and create a branch.
3. Keep the code dependency-free (Python standard library only) and match the style of `src/vram_zero.pyw`.
4. Test on Windows with an NVIDIA GPU: run `python src\vram_zero.pyw`.
5. Describe what changed and why in the pull request.

## Building

See the [README](README.md#build-from-source).

## License

By contributing, you agree that your contribution is released under the [MIT License](LICENSE).
