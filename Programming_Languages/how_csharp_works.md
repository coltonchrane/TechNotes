---
layout: default
title: How C# Works
parent: Programming Languages
nav_order: 2
date: 2026-03-24
author: coltonchrane
issue: https://github.com/coltonchrane/AutoNotes/issues/5
---

# How C# Works

This note aims to explain the fundamental workings of the C# programming language, from source code compilation to its execution within the .NET ecosystem.

## 1. Source Code and Compilation
C# is a high-level, strongly typed language. Unlike languages like C++, C# does not compile directly into machine-specific binary. Instead, when you build a C# project, the C# compiler (Roslyn) translates the source code into Common Intermediate Language (CIL), also known as Microsoft Intermediate Language (MSIL).

## 2. Assemblies and Metadata
The result of the compilation process is an assembly, typically appearing as a `.dll` or `.exe` file. These assemblies contain:
- **CIL Instructions:** Platform-independent code that describes the logic of the application.
- **Metadata:** A comprehensive manifest describing every type, method, and attribute defined in the code, as well as the external dependencies required.

## 3. The Common Language Infrastructure (CLI)
C# follows the CLI specification, which is an open standard describing the executable code and runtime environment. This allows C# to be cross-platform and inter-operable with other .NET languages (like F# or VB.NET), as they all compile down to the same intermediate language.

## 4. The Common Language Runtime (CLR)
The CLR is the "engine" that runs C# applications. When a program starts, the CLR handles the execution process. Its primary responsibilities include:
- **Loading the code:** Locating and loading assemblies into memory.
- **Security:** Verifying that the code is type-safe and follows security protocols.
- **Memory Management:** Handling the allocation and deallocation of memory.
- **Thread Management:** Managing parallel execution and CPU utilization.

## 5. Just-In-Time (JIT) Compilation
Since CIL is platform-independent, it cannot be executed directly by the CPU. The CLR includes a JIT compiler that converts CIL into native machine code (binary) specifically optimized for the host operating system and processor architecture (e.g., x64, ARM64). This compilation happens at runtime, only when a method is called for the first time.

## 6. Automatic Memory Management (Garbage Collection)
C# manages memory automatically through the Garbage Collector (GC). The GC tracks objects allocated on the "managed heap." When it detects that an object is no longer reachable by the application, it automatically reclaims that memory. This removes the need for manual memory management (like `malloc` or `free` in C), significantly reducing memory leaks and pointer-related bugs.

## 7. The Execution Flow Summary
1. **Writing Code:** Developer writes C# files (`.cs`).
2. **Compilation:** Roslyn compiles code into an assembly containing CIL and Metadata.
3. **Execution:** The user runs the application; the OS starts the .NET Runtime (CLR).
4. **JITing:** The CLR’s JIT compiler converts the CIL into native machine instructions.
5. **Runtime Services:** The CLR manages execution, providing garbage collection and type safety until the process terminates.

---
**Source/Contributor:** [coltonchrane](https://github.com/coltonchrane)
