# Contributing to OsBridgeLCCA

Thank you for considering contributing to **OsBridgeLCCA**! We welcome contributions to improve the software, fix bugs, enhance documentation, and add new features. Follow the guidelines below to ensure a smooth contribution process.

## Table of Contents
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Guidelines](#development-guidelines)
- [Code Style](#code-style)
- [Testing](#testing)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Reporting Issues](#reporting-issues)
- [License](#license)

## Getting Started

1. Fork the repository on GitHub.
2. Clone your fork to your local machine:
   ```sh
   git clone https://github.com/your-username/OsBridgeLCCA.git
   cd OsBridgeLCCA
   ```
3. Set up a virtual environment using Conda:
   ```sh
   conda create --name osbridgelcca python=3.9
   conda activate osbridgelcca
   ```
4. Install dependencies using `pyproject.toml`:
   ```sh
   pip install .
   ```

## How to Contribute

### 1. Fixing Bugs
- If you find a bug, create an issue or comment on an existing one.
- Fix the bug in a feature branch and submit a pull request.

### 2. Adding Features
- Suggest new features by opening an issue.
- Wait for maintainers' feedback before implementing major changes.
- Follow the development guidelines before submitting your PR.

### 3. Improving Documentation
- Fix typos, improve explanations, or add new documentation.
- Update `README.md`, `docs/`, or code comments where necessary.

## Development Guidelines

- Keep code modular and reusable.
- Separate frontend (`web/`), backend (`backend/`), and desktop (`desktop/`) logic.
- Store preloaded databases in `src/databases/` and user-uploaded databases in `user_databases/`.

## Code Style

- Use **PEP 8** for Python code.
- Format code using **Black**:
  ```sh
  black .
  ```
- Use **Flake8** for linting:
  ```sh
  flake8 .
  ```

## Testing

- Run unit tests with pytest:
  ```sh
  pytest tests/
  ```
- Ensure all tests pass before submitting a pull request.

## Submitting a Pull Request

1. Create a feature branch:
   ```sh
   git checkout -b feature-name
   ```
2. Make your changes and commit them:
   ```sh
   git commit -m "Description of changes"
   ```
3. Push your branch:
   ```sh
   git push origin feature-name
   ```
4. Open a pull request (PR) on GitHub.

## Reporting Issues

- Use the [Issues](https://github.com/osdag-admin/OsBridgeLCCA/issues) tab to report bugs and suggest features.
- Provide detailed descriptions and steps to reproduce bugs.

## License

OsBridgeLCCA is open-source software licensed under the [MIT License](LICENSE).

