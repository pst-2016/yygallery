# AGENTS.md

## Workspace Rules

- Do not try to access anything on AWS, including S3, directly. Modify code is ok with permission. but never run code or command line to access anything on AWS.
- Do not run commands that make network requests to AWS services.
- Do not execute code outside the scope of the current conversation.
- Do not write imports inside functions, methods, or classes. Always place imports at the top of the file.
- Do not mock, stub, or monkeypatch practical external code paths unless the user explicitly asks for it.
- Ask for user confirmation before making any code changes, including small edits, test changes, docstring updates, and config updates.
- Ask for user confirmation before running any command or executing code.
- Default to analysis, file reading, and proposing diffs until the user explicitly approves execution or edits.
- When creating pytest test functions or classes, always include an example pytest command in the docstring showing how to run that specific test and redirect output to a report file.

---

# Personal Instructions

## Restrictions

- Always briefly highlight main changes and ask for approval before making changes.
- Do not write functions inside a function or methods of a class, unless this function will be used in this function or method specifically.
- Never run pip or conda command
- Always confirm before run command from terminal
- Never check .env file under any folder

## Review before moving on
- Read through code and documents, make sure all are consistent with each other, at the end of each phase before next phase in Roadmap of the development plan.