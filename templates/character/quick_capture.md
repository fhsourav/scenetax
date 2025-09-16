---
name: "{{ name }}"
role: "{{ role }}"
status: "{{ status }}"
version: "{{ version }}"
effective_from: "{{ effective_from }}"
effective_to: "{{ effective_to }}"
date_created: "{{ date_created }}"
---

# {{ name }}

**Role:** {{ role }}
**Status:** {{ status }}
**Version:** {{ version }}
**Effective from:** {{ effective_from }}
**Effective to:** {{ effective_to }}

## Core Identity
**Age:** {{ age }}
**Profession:** {{ profession }}
**Appearance:** {{ appearance_brief }}
**First Impression:** {{ first_impression }}

## Concept
{{ concept }}

## Key Traits
- {{ trait_1 }}
- {{ trait_2 }}
- {{ trait_3 }}

## Notable Relationships
- {{ relationship_1 }}
- {{ relationship_2 }}

## Notes
{{ Notes }}
