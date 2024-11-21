
# [Source Code of Rishikeshs.com](https://github.com/rishikeshsreehari/personal-blog)

This repository contains the source code for my personal blog, built using the [Hugo](https://gohugo.io/) static site generator. The live site is available at [rishikeshs.com](https://rishikeshs.com/).

## Features

- **Custom Theme**: The blog utilizes a heavily customized version of the [Hugo PaperMod Theme](https://github.com/adityatelange/hugo-PaperMod) to suit my workflow and design preferences.
- **Content Organization**: Structured content management with archetypes and a clear directory structure for posts, pages, and other content types.
- **Automation Scripts**: Includes scripts for generating assets and managing site builds.
- **Git Hooks**: Custom Git hooks for automated tasks like changelog generation and versioning.

## Getting Started

To set up the project locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/rishikeshsreehari/personal-blog.git
   cd personal-blog
   ```

2. **Install Hugo**:  
   Ensure you have Hugo installed. Follow the [official installation guide](https://gohugo.io/getting-started/installing/) for your operating system.

3. **Run the Development Server**:
   ```bash
   hugo server
   ```
   This will start a local server at `http://localhost:1313/`, where you can view the site.

## Asset Generation

The site requires some scripts to be run for generating assets. Use the following:

- Run `scripts/build.py` to generate all required assets.  
- A GitHub Action is set up to automatically generate these assets when changes are pushed to the `main` branch.

## Hosting

The site is currently hosted on **Cloudflare Pages**. To host on Cloudflare, set the build command to:
```bash
hugo
```

## Git Hooks

This repository includes custom Git hooks defined in the `hooks` directory:

- **Pre-Push Hook**: The pre-push hook automatically generates a version number and changelog before pushing.  
  To set up the hooks directory instead of `.git/hooks`, run:
  ```bash
  ./setup-hooks.sh
  ```

## Additional Information

- **Detailed Site Information**: Visit the [Colophon](https://rishikeshs.com/colophon) for more details about this site.
- **Changelog**: The site’s changelog is available at [rishikeshs.com/log](https://rishikeshs.com/log).

## Contributing

Contributions are welcome! Feel free to fork the repository, make changes, and submit a pull request.

## License

This project is licensed under the AGPL-3.0 License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Hugo](https://gohugo.io/) for the static site generation framework.
- [Hugo PaperMod Theme](https://github.com/adityatelange/hugo-PaperMod) for the base theme.

For more information, visit [rishikeshs.com](https://rishikeshs.com/).
