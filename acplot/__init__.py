from __future__ import annotations

import string
from pathlib import Path
from typing import Any, Literal

from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.font_manager import FontManager

FontFamily = Literal["serif", "sans-serif", "cursive", "fantasy", "monospace"]
CN_FONTS: dict[FontFamily, list[str]] = {
    "serif": ["KaiTi", "STKaiti", "FandolKai", "Noto Serif CJK SC"],
    "sans-serif": ["Noto Sans CJK SC"],
}


class acplot:
    name: str
    save_formats: list[str]
    dark: bool
    kwargs: dict[str, Any]
    save_dir = Path(".")
    fig: Figure | None = None

    def __init__(
        self,
        name: str,
        save: str | list[str] | bool = False,
        save_dir: Path | None = None,
        dark: bool = False,
        font_family: FontFamily = "serif",
        **kwargs,
    ) -> None:
        self.name = name
        self.dark = dark
        self.kwargs = kwargs
        if save_dir is not None:
            self.save_dir = save_dir
        stylesheets = [Path(__file__).parent / "default.mplstyle"]
        if dark:
            stylesheets.append("dark_background")
        self.style_context = plt.style.context(stylesheets)
        if save is True:
            self.save_formats = ["pdf"]
        elif save is False:
            self.save_formats = []
        elif isinstance(save, str):
            self.save_formats = [save]

        self.font_family = [font_family]
        supported_fonts = set(
            f.name
            for f in FontManager().ttflist
            if f.name in CN_FONTS.get(font_family, [])
        )
        self.font_family.extend(supported_fonts)

        if "figsize_cm" in kwargs:  # cm to inch
            kwargs["figsize"] = tuple(x / 2.54 for x in kwargs.pop("figsize_cm"))

    def __enter__(self):
        plt.close(self.name)
        self.style_context.__enter__()
        plt.rc("font", family=self.font_family)
        self.fig = plt.figure(self.name, **self.kwargs)
        return self.fig

    def __exit__(self, exc_type, exc_value, traceback):
        if self.fig is not None:
            for img_format in self.save_formats:
                self.savefig(
                    self.name,
                    img_format=img_format,
                    fig=self.fig,
                    save_dir=self.save_dir,
                    transparent=not self.dark,
                )
            plt.show()
        self.style_context.__exit__(exc_type, exc_value, traceback)

    @staticmethod
    def savefig(
        name: str,
        img_format: str = "pdf",
        fig: Figure | None = None,
        save_dir: Path = Path("."),
        transparent: bool = True,
    ):
        if not save_dir.exists():
            save_dir.mkdir(parents=True)
        file_path = save_dir / f"{name}.{img_format}"
        kwargs = {}
        if img_format == "pdf":
            kwargs["metadata"] = {"CreationDate": None}
        (fig or plt).savefig(file_path, transparent=transparent, **kwargs)

    @staticmethod
    def merge_legends(*axes):
        handles = []
        for ax in axes:
            handles.extend(ax.get_legend_handles_labels()[0])
        return handles

    @staticmethod
    def merge_draw_legends(ax, *axes):
        handles = acplot.merge_legends(ax, *axes)
        ax.legend(handles=handles)

    @staticmethod
    def label_axes(axes=None, xytext=(-0.2, 0.4)):
        if axes is None:
            axes = plt.gcf().axes
        for i, ax in enumerate(axes):
            ax.annotate(
                string.ascii_letters[i],
                xy=(0, 1),
                xytext=xytext,
                xycoords="axes fraction",
                textcoords="offset fontsize",
                horizontalalignment="right",
                fontfamily="cmb10",
            )
