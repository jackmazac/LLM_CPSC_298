# Lecture 2 - Feb. 7, 2024

## Housekeeping
- NixOS
- Warp now available on Linux (& thus WSL)
- Discord invite is on Canvas
- OpenAI credits -- will use Copilot and Bard for now.

## Class Notes

<div align="center">
  <img src="./LLM_coding_process.png" width="400" height="365" />
</div>
Using Formal Methods with Type Theory, Specification, and Testing for Large Language Models (LLMs)
Integrating formal methods with type theory, specification, and testing offers exciting possibilities for improving the development and reliability of LLMs. Here's how they can be used together:

1. Type Theory:

Formal type systems: Specify precise interfaces for LLMs, defining acceptable inputs, outputs, and behaviors. This can catch errors early in development and ensure type safety, crucial for preventing unexpected outputs.
Theorem proving: Prove properties about LLM code using mathematical logic, guaranteeing correctness under certain conditions. This is particularly valuable for safety-critical applications of LLMs like code generation or medical diagnosis.
Dependent types: Link types and values, allowing dynamic checks based on input data. This can enforce specific constraints on LLM outputs depending on the input, enhancing data-driven correctness.

2. Specification:

Formal specifications: Clearly define the intended behavior of the LLM using languages like Z or TLA+. This serves as a reference point for development, testing, and verification.
Model checking: Verify if the LLM implementation adheres to the formal specification using automated tools. This helps identify potential inconsistencies between design and implementation.
Contract-based programming: Specify expectations for LLM inputs and outputs as contracts. These contracts can be automatically checked during training and usage, improving robustness.

3. Testing:

Symbolic execution: Explore all possible execution paths of the LLM code symbolically, identifying potential corner cases and vulnerabilities. This is especially useful for uncovering edge cases that traditional testing might miss.
Property-based testing: Generate test cases based on desired properties of the LLM, ensuring diverse and relevant testing coverage. This helps uncover hidden biases and unexpected outputs.
Fuzz testing: Feed the LLM with random or malformed inputs to test its robustness and resilience to unexpected data. This helps identify potential security vulnerabilities and data handling issues.
Challenges and Opportunities:

Integrating these methods with LLMs presents challenges:

Complexity: LLMs are inherently complex, making formalization and verification non-trivial.
Scalability: Applying formal methods across large LLM architectures can be computationally expensive.
Evolving nature: LLMs are constantly learning and evolving, making verification a moving target.
Despite these challenges, the potential benefits are significant:

Enhanced reliability: Formal methods can significantly reduce errors and guarantee certain correctness properties.
Improved transparency: Formal specifications and proofs can make LLM behavior more understandable and interpretable.
Safer applications: Formal methods can mitigate risks associated with deploying LLMs in critical applications.
Overall, the combination of formal methods with type theory, specification, and testing holds immense promise for creating more reliable, robust, and trustworthy LLMs. As research in this area progresses, we can expect significant advancements in the development and deployment of these powerful language models.

4. Integrating Software Toolchains

Tools such as git help in backtracking. With coding assistance, being able to track previously working revisions of code is key. Using linters is also critical because LLMs do not always produce syntantically or semantically correct code. 


## For Lecture
- Testing use of Discord
- Chat-GPT 4 use of Aider & OpenAI
- Notes and assignments on GitHub
- GitHub centric problems

## Examples
### TypeScript Example with Type Theory

** Scenario:** You're building a TypeScript web application requiring user authentication. You want LLM help to write secure code.

** Prompt:**

"Write a function in TypeScript to handle user login using secure password hashing. Define interfaces for User, LoginCredentials, and HashedPassword. Ensure type safety to prevent common security vulnerabilities like SQL injection."

** LLM with Type Inference: **

Similar to the Python example, this LLM can infer basic types but relies on external information for security. It defines interfaces for `User`, `LoginCredentials`, and `HashedPassword`:

```typescript
interface User {
  username: string;
  password: string; // This could be improved to a SecureString type
}

interface LoginCredentials {
  username: string;
  password: string;
}

interface HashedPassword {
  // Type details specific to the chosen hashing algorithm
}
```

It then generates the login function with basic type annotations:

```typescript
function login(credentials: LoginCredentials): boolean {
  const hashedPassword: HashedPassword = hashPassword(credentials.password); // Consult type library for secure hashing
  // ... (code to compare hashedPassword with stored value)
}
```

**LLM with Advanced Type Knowledge:**

This LLM goes further, leveraging type theory for enhanced security:

```typescript
interface Email {
  value: string; // Enforce email format validation
}

interface SecureString {
  value: string; // Enforce password length, character requirements, etc.
}

interface HashedPassword {
  algorithm: string;
  value: string;
}

function login(credentials: { username: Email; password: SecureString }): boolean {
  const hashedPassword: HashedPassword = secureHashPassword(credentials.password);
  // ... (code with explicit type checks for security-sensitive operations)
}
```

**Benefits of Type Theory in TypeScript:**

* **Stronger type safety:** TypeScript's structural typing enforces stricter type constraints compared to Python's dynamic typing.
* **Built-in type features:** TypeScript's interfaces, generics, and optional types enable more expressive and secure type definitions.
* **Improved developer experience:** Clear type annotations enhance code readability and maintainability.

**Challenges and Future Directions:**

* LLMs need training on large TypeScript codebases with robust type annotations.
* Integrating type theory concepts like dependent types into LLMs could offer even stronger guarantees.

This example demonstrates how type theory can contribute to secure and well-structured code in TypeScript with LLM assistance. As LLMs become more adept at understanding and utilizing type systems, they can become valuable tools for developers seeking to write secure and maintainable TypeScript applications.

## Homework
- hook into Discord (instructions to be provided via Discord)
- Use your preferred language to improve the sample code above with `SecureString`. Submit a pull request with your code to your own forked repo and mark me as a reviewer. Assignment is due by this coming Monday the 12th at 7PM.
- Read Formal Specification Link Below (before next lecture)

## References:
- [Formal Specifcation Example](formalspec.md)
- [Retrieval Augmented Language Models](https://www.youtube.com/watch?v=mE7IDf2SmJg)
