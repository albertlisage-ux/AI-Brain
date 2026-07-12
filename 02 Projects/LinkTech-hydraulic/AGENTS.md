# LinkTech-hydraulic Project Agent

## Project Identity

- **Brand**: HydraTec / LinkTec
- **Production domain**: `https://www.eurohydraulicparts.com/`
- **Stack**: PHP 7.4+, MySQL/MariaDB, Apache/LAMP, Tailwind CSS (CDN), vanilla JavaScript
- **Key libraries**: Swiper.js, Chart.js, Font Awesome

## Repository Structure

| Path | Purpose |
|------|---------|
| `code/hydraulich/` | Main public site, product system, support page, generator, assets, language files |
| `code/hydraulich/products/` | Source product folder tree |
| `code/hydraulich/productsPages/` | Category pages and generated product pages |
| `code/hydraulich/templates/` | Source templates for product/category generation |
| `code/users/` | Customer login, registration, dashboard, profile, ticket views |
| `code/adminmanager/` | Admin login, ticket manager, dashboard, diagnostics, user management |
| `code/config/` | Shared database, mail, security, admin, language configuration |

## Knowledge References

| Topic | File |
|-------|------|
| Project overview & skill entry | `linktec.md` |
| Frontend taste rules | `../../03 Skills/linktec-frontend-taste.md` |
| User & ticket system | `../../05 Architecture/linktech-user-system.md` |
| Product system | `../../05 Architecture/linktech-product-system.md` |
| Deployment & operations | `../../05 Architecture/linktech-deployment.md` |
| Security & credentials | `../../06 Decisions/linktech-security.md` |
| Changelog | `../../07 Lessons/linktech-changelog.md` |
| Troubleshooting | `../../07 Lessons/linktech-troubleshooting.md` |

## Active Template

- Product detail template: `code/hydraulich/templates/product-page-template-industrial-v3.php`
- The `--industrial` flag is removed; do not use it in any commands or documentation.

## Common Commands

```bash
# PHP syntax check
php -l code/hydraulich/path/to/file.php

# Product page generation (dry-run first!)
php code/hydraulich/generate_product_pages.php --dry-run
php code/hydraulich/generate_product_pages.php --status
php code/hydraulich/generate_product_pages.php --force
```

## Development Rules

1. **Update source templates first**, then regenerate affected product pages.
2. Use product image URLs returned by shared helpers directly — do not prepend duplicate product paths.
3. Keep docs and skills free of real passwords, SMTP credentials, tokens, and private server secrets.
4. Use `eurohydraulicparts.com` for current production URLs.
5. Prefer small, scoped PHP changes and run `php -l` on changed PHP files.
6. Preserve user-auth, admin-auth, and ticket ownership boundaries.
7. For public frontend/product UI styling, read the frontend taste rules before changing layout, typography, motion, imagery, or cards.
8. **Do not reintroduce** legacy `SagePi`, `visionarysagepi.com`, or HMI-only wording.
9. Source folder shape: `code/hydraulich/products/{CATEGORY}/{PRODUCT}/` with `Hero/`, `List/`, `Preview/`, `docs/` subfolders.
