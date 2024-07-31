import os
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from lia import AlignLeaf, ExtractLeaf, GetFvFm, MakeGraph, Pickcell


def main():
    test_get_fvfm()


def test_extract_leaf():
    start = time.time()
    el = ExtractLeaf()
    imgs, cnts = el.get_by_thresh("example/1-L.JPG")
    end = time.time()
    print("extract leaf time: ", end - start)
    return imgs, cnts


def test_extract_leaf_fvfm():
    start = time.time()
    el = ExtractLeaf()
    imgs, cnts = el.get_by_thresh("example/1-F.bmp")
    end = time.time()
    print("extract leaf fvfm time: ", end - start)
    return imgs, cnts


def test_extract_leaf_by_color():
    start = time.time()
    el = ExtractLeaf()
    imgs, cnts = el.get_by_color("example/1-L.JPG")
    end = time.time()
    print("extract leaf by color time: ", end - start)
    return imgs, cnts


def test_get_fvfm():
    start = time.time()
    gf = GetFvFm()
    color, value = gf.get_list("example/1-F.bmp")
    end = time.time()
    print("extract fvfm time: ", end - start)
    return color, value


def test_align():
    leaf_imgs, leaf_cnts = test_extract_leaf()
    fvfm_imgs, fvfm_cnts = test_extract_leaf_fvfm()
    start = time.time()
    al = AlignLeaf()
    fvfm_img, leaf_img = al.horizontal(
        fvfm_imgs[0], leaf_imgs[0], fvfm_cnts[0], leaf_cnts[0]
    )
    end = time.time()
    print("extract align time: ", end - start)
    return fvfm_img, leaf_img


def test_pickcell():
    fvfm_img, leaf_img = test_align()
    color, value = test_get_fvfm()
    start = time.time()
    pc = Pickcell()
    leaf_color, fvfm_color, fvfm_value = pc.pick_fvfm(leaf_img, fvfm_img, color, value)
    end = time.time()
    print("extract leaf time: ", end - start)
    return leaf_color, fvfm_color, fvfm_value


def test_graph():
    leaf_color, fvfm_color, fvfm_value = test_pickcell()
    start = time.time()
    mg = MakeGraph()
    fig_fvfm2d, fig_color3d, fig_fvfm3d, fig_multi = mg.make_color_and_fvfm(
        leaf_color, fvfm_value, "Test Sample"
    )
    end = time.time()
    print("extract leaf time: ", end - start)
    fig_multi.show()
    return fig_fvfm2d, fig_color3d, fig_fvfm3d, fig_multi


if __name__ == "__main__":
    main()
