from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path

import scienceplots  # NOQA
from matplotlib import pyplot as plt

save_dir = Path(".")

plt.style.use(["science", Path(__file__).parent / "default.mplstyle"])


def savefig(name: str, img_format: str = "pdf"):
    file_path = save_dir / f"{name}.{img_format}"
    metadata = {}
    if img_format == "pdf":
        metadata["CreationDate"] = None
    plt.savefig(file_path, metadata=metadata)


@contextmanager
def figure(
    name: str,
    save: str | list[str] | bool = False,
    figsize: tuple[int, int] | None = None,
    **kwargs,
) -> None:
    plt.close(name)
    yield plt.figure(name, figsize=figsize, **kwargs)
    if save:
        if save is True:
            save = ["pdf"]
        elif isinstance(save, str):
            save = [save]
        for img_format in save:
            savefig(name, img_format)
    plt.show()


def merge_legends(*axes):
    handles = []
    for ax in axes:
        handles.extend(ax.get_legend_handles_labels()[0])
    return handles


def merge_draw_legends(ax, *axes):
    handles, _ = ax.get_legend_handles_labels()
    for _ax in axes:
        handles.extend(_ax.get_legend_handles_labels()[0])
    ax.legend(handles=handles)
