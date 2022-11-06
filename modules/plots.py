import matplotlib.pyplot as plt
from matplotlib import ticker


def create_figure(n_subplots=1, size=3) -> (plt.Figure, tuple):
	if n_subplots == 1:
		fig, ax = plt.subplots(figsize=size, facecolor="white", constrained_layout=True)
		return fig, ax
	elif n_subplots == 2:
		fig, (ax_1, ax_2) = plt.subplots(2, 1, figsize=(size, size), facecolor="white", constrained_layout=True)
		return fig, (ax_1, ax_2)
	elif n_subplots == 3 or n_subplots == 4:
		fig, ((ax_1, ax_2), (ax_3, ax_4)) = plt.subplots(2, 2,
														 figsize=(size, size), facecolor="white",
														 constrained_layout=True)
		if n_subplots == 3:
			fig.delaxes(ax_4)
			return fig, (ax_1, ax_2, ax_3)
		return fig, (ax_1, ax_2, ax_3, ax_4)
	else:
		raise Exception("Error occurred when creating Figure. Supported number of subplots : 1,2,3,4")


def add_scatter(ax, x_t, colors, size=10, alpha=1, hide_ticker=True, text=None):
	x, y = x_t.T
	ax.scatter(x, y, c=colors, s=size, alpha=alpha)
	ax.set_title(text)
	if hide_ticker:
		ax.xaxis.set_major_formatter(ticker.NullFormatter())
		ax.yaxis.set_major_formatter(ticker.NullFormatter())
	return ax


def bench_neighbors(isomaps: list, colors, file_prefix, title=None, savefig=False):
	if len(isomaps) != 4:
		raise Exception(f"test_neighbors: Expected 4 Isomaps, received {len(isomaps)}")
	fig, (ax1, ax2, ax3, ax4) = create_figure(n_subplots=4)
	fig.suptitle(file_prefix)
	add_scatter(ax1, isomaps[0], colors, text=title[0])
	add_scatter(ax2, isomaps[1], colors, text=title[1])
	add_scatter(ax3, isomaps[2], colors, text=title[2])
	add_scatter(ax4, isomaps[3], colors, text=title[3])
	plt.show()
	plt.savefig(f"results/{file_prefix}.png") if savefig else None
