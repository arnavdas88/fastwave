# Contribution Guide

Thank you for considering contributing to our project! We welcome contributions from the community and value the time and effort put into improving the project. This guide outlines the steps to follow when contributing.

## Table of Contents

- [Getting Started](#getting-started)
  - [Fork the Repository](#fork-the-repository)
  - [Create a Branch](#create-a-branch)
- [Coding Guidelines](#coding-guidelines)
  - [Code Formatting](#code-formatting)
  - [Testing](#testing)
- [Submitting a Pull Request](#submitting-a-pull-request)
  - [Create a Pull Request](#create-a-pull-request)
  - [Code Review](#code-review)

## Getting Started

### Fork the Repository

Before you start contributing, you need to fork the repository to your GitHub account. Click the "Fork" button on the top right of the repository page.

### Create a Branch

To keep your changes isolated and organized, create a new branch for your contribution. Naming conventions for branches may vary, but it's recommended to name them in a way that reflects the purpose of your changes.

```bash
git checkout -b feature/new-feature
```

If you're fixing a bug, you might name your branch:

```bash
git checkout -b bugfix/issue-fix
```

## Coding Guidelines

### Code Formatting

Before creating a pull request, make sure your code follows the formatting standards. We use `nox` to automate the formatting process. Run the following command to format your code:

```bash
nox -e format
```

This ensures consistency and makes the codebase more maintainable.

### Testing

Ensure that your changes are backed by tests. Write tests to cover the functionality you are adding or modifying. Run the test suite locally to make sure everything is passing.

```bash
nox -e tests
```

## Submitting a Pull Request

### Create a Pull Request

Once you have made your changes and are ready to contribute them back to the main project, follow these steps:

1. Push your changes to your forked repository:

   ```bash
   git push origin your-branch-name
   ```

2. Visit your fork on GitHub and click the "Compare & pull request" button.

3. Fill out the pull request template with relevant information, including a brief description of your changes.

4. Submit the pull request.

### Code Review

Your pull request will be reviewed by the maintainers. Be responsive to feedback and make any necessary changes. Once approved, your changes will be merged into the main repository.

Thank you for contributing!
Happy Coding 😄
