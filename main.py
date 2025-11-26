# to run: `mamba activate manim` `manim -pqh main.py GenSymm`


import random

from manim import *

import decomp


class GenSymm(Scene):
    def create_numbered_squares(self, perm, side_length=0.2, buff=0.3):
        """
        Create n squares labeled perm[0]+1...perm[n-1]+1 arranged horizontally.

        Returns:
            VGroup of squares (each square is itself a VGroup of the shape + label)
        """
        squares = VGroup()
        for k in perm:
            square = Square(side_length=side_length)
            label = Text(str(k + 1)).scale(0.3)
            group = VGroup(square, label)
            label.move_to(square.get_center())
            squares.add(group)

        squares.arrange(RIGHT, buff=buff)
        return squares

    def swap_squares(self, squares: VGroup, i: int, j: int, run_time=1):
        """
        Animate swapping the squares at 0-indexed positions i and j.
        """

        sq_i = squares[i]
        sq_j = squares[j]

        # Save original positions
        pos_i = sq_i.get_center()
        pos_j = sq_j.get_center()

        # Animation: move each to the other's position
        self.play(
            sq_i.animate.move_to(pos_j),
            sq_j.animate.move_to(pos_i),
            run_time=run_time,
        )

        # Actually swap them inside the VGroup so that future swaps use correct positions
        squares.submobjects[i], squares.submobjects[j] = (
            squares.submobjects[j],
            squares.submobjects[i],
        )

    def shift_right_cycle(self, squares: VGroup, run_time=1):
        """
        Smoothly moves:
            - square at position i → i+1
            - last square → first position
        All squares move simultaneously.

        This performs a right cyclic shift.
        """
        n = len(squares)

        # Save current positions
        old_positions = [sq.get_center() for sq in squares]

        # Compute target positions
        new_positions = [None] * n
        for i in range(1, n):
            new_positions[i - 1] = old_positions[i]
        new_positions[-1] = old_positions[-0]

        # Play animations simultaneously
        self.play(
            *[squares[k].animate.move_to(new_positions[k]) for k in range(n)],
            run_time=run_time,
        )

        # Update internal ordering
        last = squares.submobjects[-1]
        squares.submobjects = [last] + squares.submobjects[:-1]

    def sort_transpos(self, perm, squares: VGroup):
        transpos = decomp.decomp_transpos(perm)
        for transpo in transpos:
            self.swap_squares(squares, transpo[0], transpo[1])
            self.wait(0.5)

    def sort_adjacent_transpos(self, perm, squares: VGroup):
        transpos = decomp.decomp_adjacent_transpos(perm)
        for transpo in transpos:
            self.swap_squares(squares, transpo[0], transpo[1])

    def sort_ct(self, perm, squares: VGroup):
        ct = decomp.decomp_ct(perm)

        for sigma in ct:
            if sigma == "t":
                self.swap_squares(squares, 0, 1, run_time=0.5)
            else:
                for _ in range(sigma):
                    self.shift_right_cycle(squares, run_time=0.5)

    def animate(self, n, label, sort_function):
        perm = list(range(n))

        random.shuffle(perm)
        squares = self.create_numbered_squares(perm)
        self.play(FadeIn(squares))
        label = Text(label).scale(0.2)
        label.next_to(squares, DOWN, buff=0.4)
        self.play(FadeIn(label))
        self.wait(1)
        sort_function(perm, squares)
        self.play(FadeOut(label))
        self.play(FadeOut(squares))

    def display_title(self, text):
        title = Tex(text).scale(0.35)
        title.move_to(ORIGIN)  # Center of the screen
        self.play(FadeIn(title))
        self.wait(3)
        self.play(FadeOut(title))

    def construct(self):
        n = 8

        self.display_title(
            r"Fact \#1: The symmetric group $\mathfrak S_n$ is generated \\ by the transpositions $[12],[13],\dots,[1n]$."
        )

        self.animate(
            n,
            "sorting the boxes by only swapping the\nleftmost box with another box",
            self.sort_transpos,
        )

        self.display_title(
            r"Fact \#2: The symmetric group $\mathfrak S_n$ is generated \\ by the transpositions $[12],[23],\dots,[n-1,n]$."
        )

        self.animate(
            n,
            "sorting the boxes by only swapping two adjacent boxes",
            self.sort_adjacent_transpos,
        )

        self.display_title(
            r"Fact \#3: The symmetric group $\mathfrak S_n$ is generated \\ by the cycles $[12]$ and $[123\dots n]$."
        )

        self.animate(
            n,
            "sorting the boxes by only swapping the first two\nboxes, and rotating all the boxes to the right",
            self.sort_ct,
        )
