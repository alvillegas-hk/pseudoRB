from playwright.sync_api import Page

def submit_form(page: Page) -> None:
    page.evaluate(
        """
        () => {
            const btn =
              document.querySelector("button[type='submit']") ||
              document.querySelector("#action");
            if (!btn) throw new Error("Botón submit no encontrado");
            btn.click();
        }
        """
    )
