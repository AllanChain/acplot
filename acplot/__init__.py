from __future__ import annotations

import string
from pathlib import Path
from typing import Any

from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.font_manager import FontManager

CN_FONTS = ["KaiTi", "FandolKai", "Noto Serif CJK SC"]


class figure:
    name: str
    save_formats: list[str]
    kwargs: dict[str, Any]
    save_dir = Path(".")
    fig: Figure | None = None

    def __init__(
        self,
        name: str,
        save: str | list[str] | bool = False,
        save_dir: Path | None = None,
        **kwargs,
    ) -> None:
        self.name = name
        self.kwargs = kwargs
        if save_dir is not None:
            self.save_dir = save_dir
        self.style_context = plt.style.context(
            Path(__file__).parent / "default.mplstyle"
        )
        if save is True:
            self.save_formats = ["pdf"]
        elif save is False:
            self.save_formats = []
        elif isinstance(save, str):
            self.save_formats = [save]

        self.font_family = ["serif"]
        supported_fonts = set(
            f.name for f in FontManager().ttflist if f.name in CN_FONTS
        )
        self.font_family.extend(supported_fonts)

    def __enter__(self):
        plt.close(self.name)
        self.style_context.__enter__()
        plt.rc('font', family=self.font_family)
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
                )
            plt.show()
        self.style_context.__exit__(exc_type, exc_value, traceback)

    @staticmethod
    def savefig(
        name: str,
        img_format: str = "pdf",
        fig: Figure | None = None,
        save_dir: Path = Path("."),
    ):
        if not save_dir.exists():
            save_dir.mkdir(parents=True)
        file_path = save_dir / f"{name}.{img_format}"
        kwargs = {}
        if img_format == "pdf":
            kwargs["metadata"] = {"CreationDate": None}
        (fig or plt).savefig(file_path, **kwargs)

    @staticmethod
    def merge_legends(*axes):
        handles = []
        for ax in axes:
            handles.extend(ax.get_legend_handles_labels()[0])
        return handles

    @staticmethod
    def merge_draw_legends(ax, *axes):
        handles = figure.merge_legends(ax, *axes)
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
            )
