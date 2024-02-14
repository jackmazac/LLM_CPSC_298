# Lecture 2 - Feb. 14, 2024

## Housekeeping
- [How to hook in Discord](https://gist.github.com/SGTGunner/50d6a3cc0d489cf779f77695ba3e22ea)
- AzureAI - credit usage being determined
- GitHub collaborators; I will need to accept your invite.
- Setting up Aider
- May be using local LLM training w/Aider (poll)
- Still working on NixOS Flake
- Class lecture videos to be posted in link on Discord/Canvas. DM me if you need last weeks lecture.
- Quiz to be placed on Discord/Canvas...
- Where everyone should be:
- * Core repo cloned and forked; ssh keys setup
- * Aider installed
- * Added GitHub user jeffrey-l-turner to your forked repo
- * Discord CI channel notifications for push pull
- * Pull Request for homework submitted to YOUR fork, not mine...
- * If on Windows, WSL installed and used

## Class Notes - Language, Code & Symbol Manipulation

Navigating Language, Code, and Symbols: let's unleash AI-powered autocomplete by exploring the foundation upon which this future rests: the intricate relationship between language, code, and symbols. Therefore, we need to dissect the fundamental relationship between formal languages, symbolic representation, and computational semantics.

1. Understanding Large Language Models used for Coding

There is an intricate relationship between data corpora and programming languages, the role of type theory in the training of LLMs, and the formal semantics that underpin the logical structure of programming languages. We will conclude with prospective pathways that coding assistance may take in the years ahead.

2. Data Corpora and Programming Languages

The foundation of any LLM is the vast expanse of data corpora. These corpora consist of extensive collections of text, code, and symbols – the lifeblood of LLM training. The diversity and quality of these corpora significantly influence the performance of an LLM when it comes to coding assistance.

Programming languages, with their strict syntax and rich semantics, present a unique challenge for LLMs. Unlike natural language, programming languages are less tolerant of ambiguity and errors. As such, the data corpora for LLMs must be meticulously curated to represent not only the syntax but also the semantic richness of programming languages.

3. Type theory in the context of LLMs and training

Type theory plays a pivotal role in the intersection of LLMs and programming. It serves as a bridge between the strict world of mathematical logic and the flexible domain of computation. In the context of LLMs, type theory informs us about the nature of constructs and variables, guiding the model towards an understanding of valid transformations and operations within a programming language.

During the training of LLMs, type theory can be leveraged to enforce constraints that ensure the generated code not only syntactically correct but also type-safe. This involves sophisticated mechanisms where the LLM learns to infer types, recognize type errors, and provide code completions that respect the type constraints inherent in the target programming language.

4. Formal Semantics: Axiomatic, Operational, & Denotational

To further refine the capabilities of LLMs in coding assistance, we delve into the realm of formal semantics. These are the rigorous frameworks that define the meaning of programming constructs. They are not merely academic exercises but serve as essential tools for ensuring that LLMs can reason about code with mathematical precision.

Axiomatic Semantics: LLMs are given a set of axioms and inference rules, akin to teaching the rules of a game. These rules allow the models to verify whether certain properties hold before and after a piece of code is executed.

Operational Semantics: This approach gives LLMs a step-by-step playbook on how a program changes state. By understanding these transitions, LLMs can simulate the execution of code snippets, thereby predicting and suggesting the outcomes of code execution.

Denotational Semantics: The most abstract of the three, denotational semantics, equips LLMs with a high-level map, translating programming constructs to mathematical objects. This enables the models to grasp the essence of a program's behavior and provide higher-order reasoning about the code.

Each of these semantic frameworks can complement the others, providing a multi-faceted understanding that LLMs can exploit to offer precise and context-aware coding assistance.

The only programming languages that have almost complete formal specification are: Ada, Standard ML, and Scheme. Haskell, OCaml, Rholang, Spark, and F* are also on track to full formal specifation. This is important in the context of correct by construction coding techniques to be used with AI.

5. Coding Assistance Future Directions

Looking ahead, the future of coding assistance is both exciting and boundless. We are likely to witness LLMs that not only suggest syntactically correct code but also engage in real-time error correction, automatic refactoring, and even the generation of code based on high-level specifications.

Advances in type theory and formal semantics will continue to refine the predictive capabilities of LLMs, moving from mere text prediction to deep semantic understanding and reasoning. We may also anticipate a closer integration of coding assistance with software development environments, where LLMs actively participate in the software development life cycle, from design to testing, deployment, and maintenance.

In the long term, LLMs could revolutionize pair programming, becoming virtual collaborators that suggest optimal coding practices, help navigate complex codebases, and even assist in the education and training of novice programmers.

As we venture into this brave new world of code and symbol manipulation, we must remain vigilant about the ethical implications and strive to develop LLMs that not only enhance productivity but also foster a deeper understanding of the languages they help us to craft.

## References:
- [Type Theory and LLM](https://medium.com/@andrew_johnson_4/harnessing-the-power-of-type-theory-in-large-language-models-351691ca2644) {behind pay wall}
- [Aider Discord]
