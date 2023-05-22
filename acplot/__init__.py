from contextlib import contextmanager
from matplotlib import pyplot as plt
from pathlib import Path
import scienceplots  # NOQA

save_dir = Path(".")

plt.style.use(["science", Path(__file__).parent / "default.mplstyle"])


@contextmanager
def figure(name: str, save=False, figsize=(8, 6), **kwargs) -> None:
    plt.close(name)
    yield plt.figure(name, figsize=figsize, **kwargs)
    if save:
        plt.savefig(
            save_dir / f"{name}.pdf",
            dpi=150,
            metadata={"CreationDate": None},
            bbox_inches="tight",
        )
    plt.show()


def merge_legends(ax, *axes):
    handles, _ = ax.get_legend_handles_labels()
    for _ax in axes:
        handles.extend(_ax.get_legend_handles_labels()[0])
    ax.legend(handles=handles)
