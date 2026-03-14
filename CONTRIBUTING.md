# How to Contribute

This repository contains generic / service thumbnails (AI-generated or human-made).

## Adding a New Thumb

To add a new thumb:

### 1. Choose a base format

Place the original thumb in one of:

- webp/
- png/
- gif/

Example:

```
webp/plex-glow.webp
```

### 2. Create a metadata file

Create a matching file in:

```
meta/
```

Example:

```
meta/plex-glow.yml
```

Use this template:

```yaml
name: plex-glow
category: service
service: plex

creator: ai
tool: <tool-name>
model: <model-name>

animated: true
variants:
  - webp
```

Since Plex is a service, we'll use `category: service` rather than `category: generic`.
For generic thumbs, you can use the following template:

```yaml
name: router
category: generic
service: null

creator: ai
tool: <tool-name>
model: <model-name>

animated: true
variants:
  - webp
```

### 3. Add/Verify Brand Entry

If this thumb represents a real service, ensure it exists in:

```
brands.json
```

If it is a generic thumb (e.g. router, computer, airplane mode), you may omit brand entry.

### 4. Optimized Versions

You may optionally provide:

- @256 version
- @128 version

Example:

```
webp/plex-glow@256.webp
```

If optimized versions are missing, CI will generate them automatically.
CI will never overwrite existing variants.

### 5. Open a Pull Request

CI will:

- generate missing optimized sizes
- rebuild index.json
- validate structure

## Notice

By submitting an thumbnail you confirm that:

- You created the asset yourself OR
- It is derived from publicly available branding assets

You agree that the thumbnail will be distributed under the repository license.

Thumbs may be AI-generated, but contributors must ensure they do not infringe copyright or trademark restrictions beyond normal service identification usage.

Optimized versions (@256, @128) may be provided manually.

If a size variant is missing, CI will automatically generate it.

CI never overwrites existing optimized variants.
