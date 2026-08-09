"""
Mermicorn Graphic AI — Visual System Engine
============================================
Shared visual system for clothing, gaming, listings, travel cards, and branding.
"""

from __future__ import annotations

import hashlib
import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional


@dataclass(frozen=True, slots=True)
class BrandPalette:
    """Mermicorn brand color system."""
    primary: str = "#FF6B9D"      # Cherry Pink
    secondary: str = "#C44DFF"    # Lazer Purple
    accent: str = "#00FFD1"       # Mermicorn Teal
    dark: str = "#1A1A2E"         # Night Base
    light: str = "#FFFFFF"        # Clean White
    muted: str = "#8B8B9E"        # Soft Gray
    
    def to_css(self) -> str:
        return f"""--cherry-pink: {self.primary};
--lazer-purple: {self.secondary};
--mermicorn-teal: {self.accent};
--night-base: {self.dark};
--clean-white: {self.light};
--soft-gray: {self.muted};"""


@dataclass(slots=True)
class DesignToken:
    """A single design token."""
    name: str
    value: str
    category: str  # color, spacing, typography, shadow
    description: str = ""


@dataclass(slots=True)
class VisualAsset:
    """A visual asset with metadata."""
    id: str
    name: str
    asset_type: str  # logo, banner, card, icon
    width: int
    height: int
    format: str  # svg, png, webp
    path: str
    tags: list[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)


class GraphicAI:
    """
    Mermicorn Visual System Engine
    
    Generates and manages visual assets for:
    - Clothing designs (rave wear)
    - Gaming overlays
    - Product listings
    - Travel cards
    - Brand identity
    """
    
    def __init__(self, output_dir: str = "./output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.palette = BrandPalette()
        self.tokens: list[DesignToken] = []
        self.assets: list[VisualAsset] = []
        self._load_default_tokens()
    
    def _load_default_tokens(self) -> None:
        """Load default design tokens."""
        self.tokens = [
            DesignToken("space-xs", "4px", "spacing", "Extra small spacing"),
            DesignToken("space-sm", "8px", "spacing", "Small spacing"),
            DesignToken("space-md", "16px", "spacing", "Medium spacing"),
            DesignToken("space-lg", "24px", "spacing", "Large spacing"),
            DesignToken("space-xl", "32px", "spacing", "Extra large spacing"),
            DesignToken("radius-sm", "8px", "border", "Small radius"),
            DesignToken("radius-md", "16px", "border", "Medium radius"),
            DesignToken("radius-lg", "24px", "border", "Large radius"),
            DesignToken("radius-full", "9999px", "border", "Full radius"),
            DesignToken("font-display", "'Inter', sans-serif", "typography", "Display font"),
            DesignToken("font-body", "'Inter', sans-serif", "typography", "Body font"),
            DesignToken("font-mono", "'Fira Code', monospace", "typography", "Mono font"),
        ]
    
    def generate_css(self) -> str:
        """Generate CSS custom properties from palette and tokens."""
        lines = [":root {"]
        
        # Colors
        lines.append("  /* Brand Colors */")
        lines.append(f"  {self.palette.to_css().replace(chr(10), chr(10) + '  ')}")
        
        # Tokens
        for category in ["spacing", "border", "typography"]:
            lines.append(f"\n  /* {category.title()} */")
            for token in self.tokens:
                if token.category == category:
                    lines.append(f"  --{token.name}: {token.value};")
        
        lines.append("}")
        return "\n".join(lines)
    
    def create_card_template(
        self,
        title: str,
        subtitle: str = "",
        image_url: str = "",
        tags: list[str] | None = None,
    ) -> str:
        """Generate an HTML card template."""
        tags_html = ""
        if tags:
            tags_html = "".join(
                f'<span class="tag">{tag}</span>' for tag in tags
            )
        
        return f"""<div class="card">
  <div class="card-image">
    {"<img src=\"" + image_url + "\" alt=\"" + title + "\">" if image_url else '<div class="placeholder"></div>'}
  </div>
  <div class="card-body">
    <h3 class="card-title">{title}</h3>
    {f'<p class="card-subtitle">{subtitle}</p>' if subtitle else ''}
    <div class="card-tags">{tags_html}</div>
  </div>
</div>"""
    
    def create_product_listing(
        self,
        name: str,
        price: str,
        description: str,
        image_url: str = "",
        features: list[str] | None = None,
    ) -> str:
        """Generate a product listing HTML."""
        features_html = ""
        if features:
            features_html = "<ul>" + "".join(
                f"<li>{f}</li>" for f in features
            ) + "</ul>"
        
        return f"""<div class="product-listing">
  <div class="product-image">
    {"<img src=\"" + image_url + "\" alt=\"" + name + "\">" if image_url else '<div class="placeholder">Image</div>'}
  </div>
  <div class="product-info">
    <h2 class="product-name">{name}</h2>
    <p class="product-price">{price}</p>
    <p class="product-description">{description}</p>
    {features_html}
    <button class="btn btn-primary">Add to Cart</button>
  </div>
</div>"""
    
    def create_travel_card(
        self,
        destination: str,
        price: str,
        dates: str,
        highlights: list[str] | None = None,
    ) -> str:
        """Generate a travel deal card."""
        highlights_html = ""
        if highlights:
            highlights_html = "<ul>" + "".join(
                f"<li>{h}</li>" for h in highlights
            ) + "</ul>"
        
        return f"""<div class="travel-card">
  <div class="destination">{destination}</div>
  <div class="price">{price}</div>
  <div class="dates">{dates}</div>
  {highlights_html}
  <button class="btn btn-secondary">View Deal</button>
</div>"""
    
    def export_assets(self) -> dict[str, str]:
        """Export all generated assets."""
        exports = {}
        
        # Export CSS
        css_path = self.output_dir / "design-tokens.css"
        css_path.write_text(self.generate_css())
        exports["css"] = str(css_path)
        
        # Export tokens as JSON
        tokens_path = self.output_dir / "tokens.json"
        tokens_data = [
            {"name": t.name, "value": t.value, "category": t.category}
            for t in self.tokens
        ]
        tokens_path.write_text(json.dumps(tokens_data, indent=2))
        exports["tokens"] = str(tokens_path)
        
        # Export palette
        palette_path = self.output_dir / "palette.json"
        palette_data = {
            "primary": self.palette.primary,
            "secondary": self.palette.secondary,
            "accent": self.palette.accent,
            "dark": self.palette.dark,
            "light": self.palette.light,
            "muted": self.palette.muted,
        }
        palette_path.write_text(json.dumps(palette_data, indent=2))
        exports["palette"] = str(palette_path)
        
        return exports
    
    def get_stats(self) -> dict[str, Any]:
        """Get system statistics."""
        return {
            "tokens": len(self.tokens),
            "assets": len(self.assets),
            "palette_colors": 6,
            "categories": list(set(t.category for t in self.tokens)),
        }


# Standalone usage
if __name__ == "__main__":
    ai = GraphicAI()
    
    print("🎨 Mermicorn Graphic AI")
    print(f"   Tokens: {ai.get_stats()['tokens']}")
    print(f"   Palette: {ai.get_stats()['palette_colors']} colors")
    print()
    
    # Generate CSS
    css = ai.generate_css()
    print("Generated CSS:")
    print(css[:500])
    print("...")
    
    # Export
    exports = ai.export_assets()
    print(f"\nExported to: {exports}")
