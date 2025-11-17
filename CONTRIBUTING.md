# Contributing to Multi-Agent Orchestrator

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are welcome! Please open an issue with:
- Clear description of the enhancement
- Why it would be useful
- Examples of how it would work

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/multi-agent-orchestrator.git
   cd multi-agent-orchestrator
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed

4. **Test your changes**
   ```bash
   python3 test_framework.py
   ```

5. **Commit with clear messages**
   ```bash
   git commit -m "Add: Brief description of changes"
   ```

6. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## Development Guidelines

### Code Style

- Follow PEP 8 for Python code
- Use type hints where appropriate
- Write docstrings for all functions/classes
- Keep functions focused and small

### Testing

- Add tests for new features
- Ensure all tests pass before submitting PR
- Aim for >80% test coverage

### Documentation

- Update README.md if adding features
- Add docstrings to new code
- Update relevant guides (DEPLOYMENT_GUIDE.md, etc.)

### Commit Messages

Use conventional commit format:
- `Add:` for new features
- `Fix:` for bug fixes
- `Update:` for changes to existing features
- `Docs:` for documentation only changes
- `Test:` for test-only changes

## Adding New Agents

To contribute a new specialist agent:

1. Create agent definition in `.claude/agents/your_agent.md`
2. Use proper YAML frontmatter format
3. Include clear description and constraints
4. Add example usage in documentation
5. Test with various tasks

Example:
```markdown
---
name: your_agent
description: Brief description
allowed_tools: ["Read", "Write"]
model: claude-sonnet-4-5
---

Your agent's system prompt here...
```

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers
- Give and receive constructive feedback
- Focus on what's best for the community

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Publishing private information
- Unprofessional conduct

## Questions?

- Open an issue for questions
- Check existing issues/discussions first
- Be patient and respectful

## Recognition

Contributors will be recognized in:
- Repository contributors list
- Release notes for significant contributions
- CONTRIBUTORS.md file

Thank you for contributing to Multi-Agent Orchestrator!
