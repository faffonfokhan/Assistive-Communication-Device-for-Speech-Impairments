# Contributing to Assistive Communication Device

Thank you for your interest in contributing to this assistive technology project!

## Code of Conduct

This project is dedicated to helping people with speech impairments. We expect all contributors to:
- Be respectful and inclusive
- Focus on accessibility and usability
- Provide constructive feedback
- Help others learn and grow

## How to Contribute

### Reporting Issues

If you encounter bugs or have feature suggestions:

1. Check if the issue already exists in the issue tracker
2. Create a new issue with a clear title and description
3. Include steps to reproduce (for bugs)
4. Add relevant system information (OS, Python version, hardware)

### Code Contributions

1. **Fork the repository**
   ```bash
   git clone https://github.com/faffonfokhan/Assistive-Communication-Device-for-Speech-Impairments.git
   cd Assistive-Communication-Device-for-Speech-Impairments
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add docstrings to new functions/classes
   - Update documentation as needed
   - Test your changes thoroughly

4. **Run validation tests**
   ```bash
   python test_structure.py
   python demo.py  # If dependencies are installed
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Provide a clear description of changes
   - Reference any related issues
   - Include screenshots/videos for UI changes

## Development Guidelines

### Code Style

- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Keep functions focused and modular

### Documentation

- Update relevant .md files when adding features
- Add docstrings to all public functions/classes
- Include usage examples for new features

### Testing

- Test on multiple platforms if possible (Windows, Linux, macOS)
- Verify camera compatibility
- Test with and without AMD Ryzen AI hardware
- Check performance impact of changes

## Areas for Contribution

We especially welcome contributions in these areas:

### High Priority
- [ ] Improved lip reading algorithms
- [ ] Better phoneme to text mapping
- [ ] Multi-language support
- [ ] Mobile device support
- [ ] Accessibility improvements

### Medium Priority
- [ ] Alternative AI model integrations
- [ ] Performance optimizations
- [ ] UI/UX enhancements
- [ ] Additional TTS engine support
- [ ] Configuration presets

### Low Priority
- [ ] Additional documentation
- [ ] Example scripts and tutorials
- [ ] Unit tests
- [ ] Code refactoring

## Architecture Notes

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system design.

Key components:
- **Lip Detection**: Uses MediaPipe for facial landmark tracking
- **Text Processing**: Llama 2 for text generation
- **Speech Synthesis**: Multiple TTS engines
- **Hardware Acceleration**: AMD Ryzen AI optimization

## Questions?

Feel free to:
- Open an issue for questions
- Start a discussion in the repository
- Contact the maintainers

Thank you for helping make communication more accessible!
