from curses import wrapper
import curses


class RegisterWindow(object):
    HEIGHT = 10
    WIDTH = 14

    def __init__(self, parent, py, px):
        self.parent = parent
        self.win = parent.pad.subwin(RegisterWindow.HEIGHT,
                                     RegisterWindow.WIDTH,
                                     py,
                                     px)
        self.win.border()
        y = 1
        for reg in ['A', 'B', 'C', 'D', 'E', 'H', 'L']:
            self.win.addstr(y, 1, reg + ':00')
            y += 1
        self.win.addstr(1, 6, ' I:00')
        self.win.addstr(2, 6, ' R:00')
        self.win.addstr(3, 6, 'IX:0000')
        self.win.addstr(4, 6, 'IY:0000')
        self.win.addstr(5, 6, 'SP:0000')
        self.win.addstr(6, 6, 'PC:0000')
        self.win.addstr(7, 1, 'F:00000000')
        self.win.addstr(8, 1, '  ????????')


class HexdumpWindow(object):
    WIDTH = 42
    HEIGHT = 10

    def __init__(self, parent, py, px):
        self.parent = parent
        self.win = parent.pad.subwin(HexdumpWindow.HEIGHT,
                                     HexdumpWindow.WIDTH,
                                     py,
                                     px)
        self.win.border()
        value = 0
        fmtstr = '%02x: 11 22 33 44 55 66 77 88 ........'
        for line in range(1, 9):
            self.win.addstr(line, 1, fmtstr % value)
            value += 8


class MainPad(object):
    def __init__(self, parent):
        self.parent = parent
        self.pad = curses.newpad(20, 70)
        x1 = 70 - 2 * RegisterWindow.WIDTH
        x2 = 70 - RegisterWindow.WIDTH
        self.reg_window_1 = RegisterWindow(self, 0, x1)
        self.reg_window_2 = RegisterWindow(self, 0, x2)
        self.hex_window = HexdumpWindow(self, 0, 0)


class Screen(object):
    def __init__(self, screen):
        self.screen = screen
        self.width = 0
        self.height = 0
        self.screen.clear()
        self.screen.refresh()
        self.height, self.width = self.screen.getmaxyx()
        self.pad = MainPad(self)

    def refresh(self):
        self.screen.refresh()
        y, x = self.screen.getmaxyx()
        self.pad.pad.refresh(0, 0, 1, 1, y - 1, x - 1)

    def run(self):
        while True:
            c = self.screen.getch()
            if c == curses.KEY_RESIZE:
                self.refresh()


def main(stdscr):
    screen = Screen(stdscr)
    screen.refresh()
    screen.run()


wrapper(main)
