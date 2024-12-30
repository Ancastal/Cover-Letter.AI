## [Unreleased]

## [1.2.1] - 2024-01-03
### Fixed
- Added missing app.py and cover_letter_editor.py files to the release

## [1.2.0] - 2024-01-03
### Added
- New cover letter editor interface with customization options
- Tone selection (Professional, Friendly, Confident, Enthusiastic)
- Style selection (Traditional, Modern, Creative, Concise)
- Skills emphasis customization
- Length preference control
- Real-time preview of edited cover letters
- New Settings tab for managing application secrets
- Interface for configuring LinkedIn credentials
- Secure storage of credentials in .streamlit/secrets.toml

### Changed
- Enhanced README.md with version shield, improved documentation, and better formatting

## [1.1.0] - 2024-12-30
### Added
- Download button for generated cover letters
- Helpful tooltips and placeholders for input fields
- Sidebar with app information and usage instructions
- URL validation for LinkedIn URLs
- Loading spinners for better feedback
- Enhanced cover letter display with professional formatting
- Improved button styling and visual hierarchy

### Changed
- Improved UI layout with tabs for different input methods
- Streamlined field options for better focus
- Enhanced error messages and validation
- Better handling of optional profile fields
- Refined visual design with consistent spacing and typography
- Optimized layout width for better readability

### Fixed
- Removed hardcoded credentials
- Improved error handling throughout the application
- More robust profile data extraction
- Better handling of missing LinkedIn profile data
- Improved job posting scraping reliability with retry mechanism, rotating user agents, and better error handling

## [1.0.0] - 2023-06-25
### Added
- Initial release of Cover-Letter.AI
