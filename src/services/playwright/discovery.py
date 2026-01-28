import logging
from typing import List
from playwright.sync_api import Page

from .models import FormField, FormOption

log = logging.getLogger("playwright.discovery")

def discover_form_fields(page: Page) -> List[FormField]:
    raw_fields = page.evaluate(
        """
        () => {
          const elements = [];
          document.querySelectorAll('input, textarea, select').forEach(el => {
            if (el.type === 'hidden') return;

            const field = {
              tag: el.tagName.toLowerCase(),
              id: el.id || null,
              name: el.name || null,
              type: el.type || null,
              placeholder: el.placeholder || null,
              ariaLabel: el.getAttribute('aria-label'),
              text: el.innerText || null,
              options: null
            };

            if (el.tagName.toLowerCase() === 'select') {
              field.options = Array.from(el.options).map(o => ({
                value: o.value,
                label: o.text.trim()
              }));
            }

            elements.push(field);
          });
          return elements;
        }
        """
    )

    fields: List[FormField] = []

    for f in raw_fields:
        options = None
        if f.get("options"):
            options = [FormOption(**opt) for opt in f["options"]]

        fields.append(FormField(
            tag=f["tag"],
            id=f["id"],
            name=f["name"],
            type=f["type"],
            placeholder=f["placeholder"],
            aria_label=f["ariaLabel"],
            text=f["text"],
            options=options
        ))

    return fields
