# Copilot Coding Instructions

This document outlines the core principles and practices for writing high-quality, maintainable, and robust code. Follow these guidelines to ensure consistency and collaboration across the project.

***

## 🏛️ Domain-Driven Design (DDD)

Our approach is centered on the business domain. Your primary goal is to write code that clearly expresses the domain model.

* **Ubiquitous Language**: Use names for classes, methods, and variables that come directly from the business domain. If the business calls it a "Customer Mandate," don't call it a `ClientAgreement`.
* **Model the Domain**: Structure the code around core domain concepts. Help identify and create **Entities**, **Value Objects**, **Aggregates**, and **Repositories**.
* **Bounded Contexts**: Keep domain logic isolated within its specific bounded context. Avoid creating dependencies that cross these boundaries unnecessarily.
* **Focus on Behavior**: Methods on domain objects should represent real business operations, not just simple getters and setters (e.g., `customer.deactivate()` instead of `customer.setStatus('inactive')`).

***

## 🧪 Test-Driven Development (TDD)

All new functionality must be developed using a strict TDD workflow. Tests are not an afterthought; they are a fundamental part of the design process.

* **Red-Green-Refactor**: Always follow this cycle.
    1.  🔴 **Red**: Write a simple, failing test for a small piece of functionality.
    2.  🟢 **Green**: Write the *absolute minimum* amount of code required to make the test pass.
    3.  🔵 **Refactor**: Clean up the code you just wrote, ensuring it is clear, efficient, and well-designed, while all tests remain green.
* **Descriptive Tests**: Test names should clearly describe the behavior they are testing (e.g., `test_throws_exception_when_placing_order_with_insufficient_stock`).
* **One Assertion Per Test**: Ideally, each test should verify a single logical outcome.

***

## ✍️ Commenting and Code Clarity

Code should be self-documenting. Comments are the exception, not the rule.

* **No Obvious Comments**: Do not write comments that state the obvious. The code itself should make its purpose clear.
    * **Bad**: `// Increment the counter`
    * **Bad**: `i++;`
* **Explain the "Why," Not the "How"**: Use comments only when the code's purpose is not immediately clear, especially for complex or unusual business logic. Explain *why* the code is written a certain way.
    * **Good**: `// We must manually void the previous invoice due to a legacy billing`
    * **Good**: `// system requirement (Ticket #415) before issuing a new one.`
* **Meaningful Naming**: Prioritize clear, descriptive names for variables, functions, and classes over writing comments. A well-named function is better than a comment.

***

## ✨ Formatting and Style

Consistent formatting is crucial for readability.

* **Newline at End of File (EOF)**: **Always** ensure there is a single newline character at the very end of every file.
* **Line Feed (LF) Newlines**: **Always** use LF (`\n`) for line endings. Configure your environment to enforce this, even when working on Windows, to prevent version control conflicts.

***

## 🚀 Other Good Practices

Incorporate these general principles into all your work.

* **DRY (Don't Repeat Yourself)**: Avoid duplicating code. Abstract common logic into reusable functions or classes.
* **Single Responsibility Principle (SRP)**: Each function, class, or module should have one, and only one, reason to change. Keep them small and focused.
* **Immutability**: Prefer immutable data structures wherever possible. This reduces side effects and makes state management easier to reason about.
* **Dependency Injection**: Use dependency injection to decouple components and make your code easier to test and maintain.