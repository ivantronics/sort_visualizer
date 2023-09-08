from dataclasses import dataclass

import math
import random
import time

import pygame

pygame.init()


@dataclass
class DataHandler:

    lst: list
    window_width: int = 800
    window_height: int = 600

    # constants
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BLUE = 0, 0, 255
    YELLOW = 255, 225, 0
    PURPLE = 125, 0, 255
    GREY = 129, 129, 129
    BACKGROUND_COLOR = 210, 210, 210
    GRADIENTS = (
        (50, 50, 50),
        (70, 70, 70),
        (100, 100, 100),
        (140, 140, 140)
    )

    # padding
    SIDE_PAD = 50
    TOP_PAD = 160

    # small, medium and large fonts
    DFONT = pygame.font.SysFont('arial', 15, italic=True)
    FONT = pygame.font.SysFont('arial', 20)
    HFONT = pygame.font.SysFont('arial', 40)

    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Sorting Algorithms Visualizer")

    # initial options
    sequential: bool = True
    ascending: bool = True

    # prepare initial list for sorting
    def __post_init__(self):
        self.display_min = min(self.lst)
        self.display_max = max(self.lst)
        self.size = len(self.lst)
        self.lst = list(map(lambda x: x - self.display_min, self.lst))
        # calculating how many pixels each bar would occupy in x plane
        # depending on data size
        self.val_per_pixel = (self.window_height - self.TOP_PAD - 55) / (
                max(self.lst) - min(self.lst))
        self.bar_width = math.floor(
            (self.window_width - self.SIDE_PAD) / self.size)
        # start point for bars to draw from
        self.start_x = (self.window_width - self.bar_width * self.size) // 2

        # available algorithms names in dict form for info display
        self.algos = {bubble_sort: "Bubble Sort",
                      insertion_sort: "Insertion sort",
                      merge_sort: "Merge Sort",
                      quick_sort: "Quick Sort",
                      selection_sort: "Selection Sort"}
        self.algo_display = self.algos.get(bubble_sort)
        self.quick_mode = False

    def set_list(self, lst: list) -> None:
        # For recalculating the look and positions depending on new input
        self.display_min = min(lst)
        self.display_max = max(lst)
        self.size = len(lst)
        self.lst = list(map(lambda x: x - self.display_min, lst))
        self.val_per_pixel = (self.window_height - self.TOP_PAD - 55) / (
                max(lst) - min(lst))
        self.bar_width = math.floor(
            (self.window_width - self.SIDE_PAD) / self.size)
        self.start_x = (self.window_width - self.bar_width * self.size) // 2


def generate_list(n: int, min_val: int, max_val: int) -> list:
    # generating random number list depending on minimum and maximum sizes
    lst = []
    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)
    return lst


def generate_range(n: int) -> list:
    # generating a consecutive list of numbers then shuffling them
    lst = list(range(n))
    random.shuffle(lst)
    return lst


def get_list(array_size: int, min_val: int,
             max_val: int, sequential: bool) -> list:
    # returns list of consecutive or random numbers depending on a condition
    if sequential:
        lst = generate_range(array_size)
    else:
        lst = generate_list(array_size, min_val, max_val)
    return lst


def draw(dh: DataHandler) -> None:
    # main drawing loop

    # background
    dh.window.fill(dh.BACKGROUND_COLOR)

    title = "Sorting Visualizer"
    title_display = dh.HFONT.render(title, 1, dh.BLACK)
    # placing title in the middle
    dh.window.blit(title_display, (
        dh.window_width / 2 - title_display.get_width() / 2, 5))

    # info screen for users explaining controls
    controls_firstline = "R: reset array | +/-: control data size |" \
                         " S: toggle sequential"
    controls_secondline = "SPACE: start/stop sorting |" \
                          " T: ascending/descending | q: toggle quick mode"
    controls_thirdline = "1: Bubble Sort | 2: Insertion Sort | 3: Merge Sort"
    controls_fourthline = "4: Quick Sort | 5: Selection Sort | "
    controls = [controls_firstline, controls_secondline,
                controls_thirdline, controls_fourthline]
    controls_start_pos = 65
    for line in controls:
        display = dh.DFONT.render(line, 1, dh.BLACK)
        dh.window.blit(display, (10, controls_start_pos))
        controls_start_pos += 25

    # general current info display to diminish confusion
    current_data_size = f"Data size: {dh.size}"
    current_range = f"Range: from {dh.display_min} " \
                    f"to {dh.display_max}"
    current_sequential = f"{(lambda x: 'Sequential' if x else 'Non-sequential')(dh.sequential)}"
    current_ascendace = f"{(lambda x: 'Ascending' if x else 'Descending')(dh.ascending)}"
    current_algorithm = f"Current sort: {dh.algo_display}"
    quick_mode = f"Quick mode: {(lambda x: 'On' if not x else 'Off')(dh.quick_mode)}"
    info_lines = [current_data_size, current_range, current_sequential,
                  current_ascendace, current_algorithm, quick_mode]
    info_start_pos = 15
    for line in info_lines:
        display = dh.FONT.render(line, True, dh.BLACK)
        dh.window.blit(display, (
            dh.window_width - display.get_width() - 10, info_start_pos))
        info_start_pos += 25

    # execute sorting animation
    visualizer(dh)
    pygame.display.update()


def inverse_color(color: tuple) -> tuple:
    # accepts color in tuple and returns it back inverted
    inverted = []
    for i in color:
        i = abs(i - 255)
        inverted.append(i)
    return tuple(inverted)


def visualizer(dh: DataHandler, color_pos: dict = None,
               clear_bg: bool = False) -> None:
    # main loop for visualizer animation

    if color_pos is None:
        color_pos = {}

    # getting our list for sorting
    lst = dh.lst

    # redrawing background if we have condition
    if clear_bg:
        clear_rect = (dh.SIDE_PAD // 2, dh.TOP_PAD,
                      dh.window_width - dh.SIDE_PAD,
                      dh.window_height - dh.TOP_PAD)
        pygame.draw.rect(dh.window, dh.BACKGROUND_COLOR,
                         clear_rect)

    # sorting loop
    for idx, val in enumerate(lst):
        x_cor = dh.start_x + (idx * dh.bar_width)
        bar_height = round(val * dh.val_per_pixel)
        y_cor = dh.window_height - bar_height - 15
        color = dh.GRADIENTS[idx % len(dh.GRADIENTS)]
        if idx in color_pos:
            color = color_pos[idx]
        pygame.draw.rect(dh.window, color,
                         (x_cor, y_cor, dh.bar_width, bar_height + 10))
        # + 10 because we want 0 to be represented at least with 10px
        # so we shift everything including it by 10px

    # updating display if we cleared it before
    if clear_bg:
        pygame.display.update()


def bubble_sort(dh: DataHandler):
    # logic for buble sort
    lst = dh.lst
    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]
            if (num1 > num2 and dh.ascending) or \
                    (num1 < num2 and not dh.ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                visualizer(dh,
                           {j: dh.GREEN, j + 1: dh.RED},
                           True)
                yield True
    return lst


def insertion_sort(dh: DataHandler):
    # logic for insertion sort
    lst = dh.lst
    for i in range(1, len(lst)):
        current = lst[i]
        while True:
            ascending_sort = i > 0 and lst[i - 1] > current \
                             and dh.ascending
            descending_sort = i > 0 and lst[i - 1] < current \
                              and not dh.ascending
            if not ascending_sort and not descending_sort:
                break
            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            visualizer(dh,
                       {i - 1: dh.GREEN, i: dh.RED},
                       True)
            yield True
    return lst


def merge_sort(dh: DataHandler):
    # logic for merge sort
    lst = dh.lst
    width = 1
    n = len(lst)
    while width < n:
        l = 0
        while l < n:
            r = min(l + (width * 2 - 1), n - 1)
            m = min(l + width - 1, n - 1)
            visualizer(dh,
                       {l: dh.YELLOW, r: dh.PURPLE},
                       True)
            yield True
            merge(lst, l, m, r, dh)
            visualizer(dh,
                       {l: dh.YELLOW, r: dh.PURPLE},
                       True)
            yield True
            l += width * 2
        width *= 2
    return lst


def merge(lst: list, l: int, m: int, r: int, dh: DataHandler):
    # merge sort helper function

    ascending = dh.ascending
    n1 = m - l + 1
    n2 = r - m
    L = [0] * n1
    R = [0] * n2

    for i in range(0, n1):
        L[i] = lst[l + i]

    for i in range(0, n2):
        R[i] = lst[m + i + 1]

    i, j, k = 0, 0, l

    if ascending:
        while i < n1 and j < n2:
            if L[i] <= R[j]:
                lst[k] = L[i]
                visualizer(dh,
                           {k: dh.RED, l: dh.GREEN},
                           True)
                i += 1
            else:
                lst[k] = R[j]
                visualizer(dh,
                           {k: dh.RED, l: dh.GREEN},
                           True)
                j += 1
            visualizer(dh,
                       {k: dh.RED, l: dh.GREEN},
                       True)
            k += 1

        while i < n1:
            lst[k] = L[i]
            visualizer(dh,
                       {k: dh.RED, l: dh.GREEN},
                       True)
            i += 1
            k += 1

        while j < n2:
            lst[k] = R[j]
            visualizer(dh,
                       {k: dh.RED, l: dh.GREEN},
                       True)
            j += 1
            k += 1
    else:
        while i < n1 and j < n2:
            if L[i] >= R[j]:
                lst[k] = L[i]
                i += 1
            else:
                lst[k] = R[j]
                j += 1
            k += 1

        while i < n1:
            lst[k] = L[i]
            i += 1
            k += 1

        while j < n2:
            lst[k] = R[j]
            j += 1
            k += 1
    return lst


def quick_sort(dh: DataHandler):
    # logic for quick sort
    lst = dh.lst
    l = 0
    h = len(lst) - 1
    size = h - l + 1
    stack = [0] * (size)
    top = -1

    top = top + 1
    stack[top] = l

    top = top + 1
    stack[top] = h

    while top >= 0:
        h = stack[top]
        top = top - 1
        l = stack[top]
        top = top - 1
        visualizer(dh,
                   {l: dh.YELLOW, h: dh.PURPLE},
                   True)
        yield True
        visualizer(dh,
                   {l: dh.YELLOW, h: dh.PURPLE},
                   True)
        yield True
        p = partition(dh, l, h, dh.ascending)
        visualizer(dh,
                   {l: dh.YELLOW, h: dh.PURPLE},
                   True)
        yield True
        visualizer(dh,
                   {l: dh.YELLOW, h: dh.PURPLE},
                   True)
        yield True

        if p - 1 > l:
            top = top + 1
            stack[top] = l
            top = top + 1
            stack[top] = p - 1

        if p + 1 < h:
            top = top + 1
            stack[top] = p + 1
            top = top + 1
            stack[top] = h
    return lst


def partition(dh: DataHandler, l: int, h: int, ascending: bool):
    # helper function for quick sort
    lst = dh.lst
    i = (l - 1)
    x = lst[h]
    if ascending:
        for j in range(l, h):
            if lst[j] <= x:
                i = i + 1
                visualizer(dh,
                           {i: dh.RED, j: dh.GREEN},
                           True)
                lst[i], lst[j] = lst[j], lst[i]
        visualizer(dh,
                   {i + 1: dh.RED, h: dh.GREEN},
                   True)
        lst[i + 1], lst[h] = lst[h], lst[i + 1]
        return i + 1
    else:
        for j in range(l, h):
            if lst[j] >= x:
                i = i + 1
                visualizer(dh,
                           {i: dh.RED, j: dh.GREEN},
                           True)
                time.sleep(0.02)
                lst[i], lst[j] = lst[j], lst[i]
        visualizer(dh,
                   {i + 1: dh.RED, h: dh.GREEN},
                   True)
        time.sleep(0.02)
        lst[i + 1], lst[h] = lst[h], lst[i + 1]
        return i + 1


def selection_sort(dh: DataHandler):
    # logic for selection sort
    lst = dh.lst

    if dh.ascending:
        for i in range(len(lst)):
            min_idx = i
            for j in range(i + 1, len(lst)):
                visualizer(dh,
                           {i: dh.RED, min_idx: dh.GREEN},
                           True)
                if lst[min_idx] > lst[j]:
                    min_idx = j
            visualizer(dh,
                       {i: dh.RED, min_idx: dh.GREEN},
                       True)
            yield True
            lst[i], lst[min_idx] = lst[min_idx], lst[i]
    else:
        for i in range(len(lst)):
            max_idx = i
            for j in range(i + 1, len(lst)):
                visualizer(dh,
                           {i: dh.RED, max_idx: dh.GREEN},
                           True)
                if lst[max_idx] < lst[j]:
                    max_idx = j
            visualizer(dh,
                       {i: dh.RED, max_idx: dh.GREEN},
                       True)
            yield True
            lst[i], lst[max_idx] = lst[max_idx], lst[i]
    return lst
