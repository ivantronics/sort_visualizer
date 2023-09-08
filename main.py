import time

import pygame

from data_handler import DataHandler, get_list, draw, bubble_sort, \
    insertion_sort, merge_sort, quick_sort, selection_sort


def main():
    # main app loop

    run = True
    clock = pygame.time.Clock()

    # constants
    window_width, window_height = 800, 600
    array_size, min_val, max_val = 30, -10000, 10000

    sorting = False

    algo_curr = bubble_sort
    algo_gen = None

    lst = get_list(array_size, min_val, max_val, True)
    dh = DataHandler(lst, window_width, window_height)

    # pygame loop
    while run:
        clock.tick(60)

        dh.algo_display = dh.algos.get(algo_curr)

        if sorting:
            try:
                next(algo_gen)
            except StopIteration:
                sorting = False
        else:
            draw(dh)

        if dh.quick_mode:
            time.sleep(0.05)

        events = pygame.event.get()
        for event in events:

            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            # reset current list with 'r'
            if event.key == pygame.K_r and not sorting:
                lst = get_list(array_size, min_val,
                               max_val, dh.sequential)
                dh.set_list(lst)

            # increase current data size with '+'
            elif event.key == pygame.K_EQUALS and not sorting:
                array_size += 1
                lst = get_list(array_size, min_val,
                               max_val, dh.sequential)
                dh.set_list(lst)

            # decrease current data size with '-'
            elif event.key == pygame.K_MINUS and not sorting:
                array_size -= 1
                if array_size == 1:
                    array_size = 2
                lst = get_list(array_size, min_val,
                               max_val, dh.sequential)
                dh.set_list(lst)

            # change sequential option with 's'
            elif event.key == pygame.K_s and not sorting:
                dh.sequential = not dh.sequential

            # start or stop sorting with 'space'
            elif event.key == pygame.K_SPACE:
                sorting = not sorting
                algo_gen = algo_curr(dh)

            # change sorting direction with 't'
            elif event.key == pygame.K_t and not sorting:
                dh.ascending = not dh.ascending

            # toggle quick mode on or off with 'q'
            elif event.key == pygame.K_q:
                dh.quick_mode = not dh.quick_mode

            # change sorting algorithm to bubble sort with '1'
            elif event.key == pygame.K_1 and not sorting:
                algo_curr = bubble_sort

            # change sorting algorithm to insertion sort with '2'
            elif event.key == pygame.K_2 and not sorting:
                algo_curr = insertion_sort

            # change sorting algorithm to merge sort with '3'
            elif event.key == pygame.K_3 and not sorting:
                algo_curr = merge_sort

            # change sorting algorithm to quick sort with '4'
            elif event.key == pygame.K_4 and not sorting:
                algo_curr = quick_sort

            # change sorting algorithm to selection sort with '5'
            elif event.key == pygame.K_5 and not sorting:
                algo_curr = selection_sort

    pygame.quit()


if __name__ == '__main__':
    main()
