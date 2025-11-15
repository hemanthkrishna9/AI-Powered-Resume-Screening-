# Angular App

A production-ready Angular application built with the latest Angular 20 framework, featuring server-side rendering (SSR), comprehensive tooling, and best practices.

## Features

- **Angular 20** - Latest version with cutting-edge features
- **Server-Side Rendering (SSR)** - Enhanced performance and SEO
- **TypeScript** - Strict mode enabled for type safety
- **SCSS** - Modern styling with Sass
- **Routing** - Angular Router pre-configured
- **ESLint** - Code quality and consistency
- **Prettier** - Automatic code formatting
- **Jasmine & Karma** - Comprehensive testing setup
- **Environment Configurations** - Separate dev and prod configs
- **Production Optimizations** - Bundle size budgets and optimizations

## Prerequisites

- Node.js 18+ (tested with v22.21.1)
- npm 9+ (tested with v10.9.4)

## Installation

```bash
npm install
```

## Development

Start the development server:

```bash
npm start
# or
npm run dev  # Opens browser automatically
```

The application will be available at `http://localhost:4200/`

## Available Scripts

### Development
- `npm start` - Start development server
- `npm run dev` - Start development server and open browser
- `npm run watch` - Build in watch mode

### Build
- `npm run build` - Build the application
- `npm run build:prod` - Production build with optimizations
- `npm run build:ssr` - Build with server-side rendering

### Testing
- `npm test` - Run tests in watch mode
- `npm run test:ci` - Run tests once (for CI/CD)
- `npm run test:coverage` - Run tests with coverage report

### Code Quality
- `npm run lint` - Lint code with ESLint
- `npm run lint:fix` - Fix linting issues automatically
- `npm run format` - Format code with Prettier
- `npm run format:check` - Check code formatting

### Production
- `npm run serve:ssr` - Serve SSR application
- `npm run precommit` - Format and lint before commit
- `npm run validate` - Run all checks (format, lint, test, build)

## Project Structure

```
angular-app/
├── src/
│   ├── app/                 # Application components
│   │   ├── app.ts          # Root component
│   │   ├── app.config.ts   # App configuration
│   │   └── app.routes.ts   # Route definitions
│   ├── environments/        # Environment configurations
│   │   ├── environment.ts      # Development config
│   │   └── environment.prod.ts # Production config
│   ├── main.ts             # Application entry point
│   ├── main.server.ts      # SSR entry point
│   ├── server.ts           # Express server for SSR
│   ├── index.html          # HTML template
│   └── styles.scss         # Global styles
├── public/                  # Static assets
├── angular.json            # Angular CLI configuration
├── tsconfig.json           # TypeScript configuration
├── eslint.config.js        # ESLint configuration
└── package.json            # Dependencies and scripts
```

## Environment Configuration

The app uses environment-specific configurations:

- **Development**: `src/environments/environment.ts`
- **Production**: `src/environments/environment.prod.ts`

Modify these files to configure API endpoints, feature flags, and other environment-specific settings.

## Building for Production

Build the application for production:

```bash
npm run build:prod
```

The build artifacts will be stored in the `dist/` directory.

### SSR Build

For server-side rendering in production:

```bash
npm run build:ssr
npm run serve:ssr
```

## Code Quality Standards

This project enforces code quality through:

1. **TypeScript Strict Mode** - Enhanced type checking
2. **ESLint** - Consistent code style and error prevention
3. **Prettier** - Automatic code formatting
4. **Bundle Size Budgets** - Prevents bundle bloat
   - Initial bundle: 500kB warning, 1MB error
   - Component styles: 4kB warning, 8kB error

## Testing

Run the test suite:

```bash
npm test
```

For CI/CD pipelines:

```bash
npm run test:ci
```

Generate coverage report:

```bash
npm run test:coverage
```

## Code Scaffolding

Angular CLI includes powerful code scaffolding tools. To generate a new component:

```bash
ng generate component component-name
```

For a complete list of available schematics (such as `components`, `directives`, or `pipes`):

```bash
ng generate --help
```

## Contributing

1. Format your code: `npm run format`
2. Fix linting issues: `npm run lint:fix`
3. Run tests: `npm test`
4. Build: `npm run build:prod`

Or run all checks at once:

```bash
npm run validate
```

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Performance

The application includes:

- Lazy loading routes
- Production build optimizations
- Server-side rendering for faster initial load
- Bundle size monitoring and budgets

## Additional Resources

- [Angular CLI Overview and Command Reference](https://angular.dev/tools/cli)
- [Angular Documentation](https://angular.dev)
- This project was generated using [Angular CLI](https://github.com/angular/angular-cli) version 20.3.10
