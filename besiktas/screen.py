from datetime import datetime
from time import sleep

from rich import box
from rich.align import Align
from rich.console import Group
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .scrapper import Scraper


class Application:
    def __init__(self):
        self.scrapper = Scraper()
        self.layout = Layout(name="root")
        self.layout.split(
            Layout(name="header", ratio=3),
            Layout(name="main", ratio=12),
            Layout(name="footer", ratio=1),
        )
        self.layout["header"].split_row(
            Layout(name="header-left", ratio=1),
            Layout(name="header-middle", ratio=3),
            Layout(name="header-right", ratio=1),
        )
        self.layout["main"].split_row(
            Layout(name="main-left", ratio=1),
            Layout(name="main-middle", ratio=1),
            Layout(name="main-right", ratio=1)
        )

    def setup(self):
        self.layout["header-left"].update(self.get_header_left())
        self.layout["header-middle"].update(self.get_header_middle())
        self.layout["header-right"].update(self.get_header_right())
        self.layout["main-left"].update(self.get_main_left())
        self.layout["main-middle"].update(self.get_main_middle())
        self.layout["main-right"].update(self.get_main_right())
        self.layout["footer"].update(self.get_footer())

    def run(self):
        with Live(self.layout, screen=True):
            while True:
                sleep(1)

    def get_header_left(self):
        cups = Table.grid(expand=True)
        cups.add_column(style="bold")
        cups.add_column()
        cups.add_column()
        for count, title in self.scrapper.cups:
            cups.add_row(count, " ", title)
        return Panel(Align.center(cups, vertical="middle"))

    @staticmethod
    def get_header_middle():
        logo = Group(
            Align.center("[black]Besik[/black][white]tas[/white]\n"),
            Align.center("1905"),
        )
        return Panel(Align.center(logo, vertical="middle"), style="bold", padding=1)

    def get_header_right(self):
        return Panel(Align.center(f"Kadro değeri\n[b]{self.scrapper.team_value}[/b]", vertical="middle"))

    def get_main_left_top(self):
        standings = Table(expand=True, box=box.SIMPLE)
        standings.add_column(header="#")
        standings.add_column(header="Kulüp")
        standings.add_column(header="Maçlar")
        standings.add_column(header="+/-")
        standings.add_column(header="Puan")

        for no, club, matches, average, points, highlight in self.scrapper.standings:
            style = "u red on white" if highlight else None
            standings.add_row(no, club, matches, average, points, style=style)
        return Panel(standings, title="[cyan][b]TABLO KESİTİ SÜPER LİG[/b][/cyan]", box=box.SQUARE)

    def get_main_left_bottom(self):
        truths = Table.grid(expand=True)
        truths.add_column()
        truths.add_column()
        truths.add_column()
        tr = self.scrapper.truths
        truths.add_row("Resmi kulüp adı", ": ", tr["legal_name"])
        truths.add_row("Adres", ": ", tr["address"])
        truths.add_row("Tel", ": ", tr["telephone"])
        truths.add_row("Faks", ": ", tr["fax"])
        truths.add_row("Web sayfası", ": ", tr["url"])
        truths.add_row("Kuruluş", ": ", tr["founded"])
        truths.add_row("Üyeler", ": ", tr["members"])
        return Panel(truths, title="[cyan][b]VERİLER & GERÇEKLER[/b][cyan]", box=box.SQUARE)

    def get_main_left(self):
        left_top = self.get_main_left_top()
        left_bottom = self.get_main_left_bottom()
        return Panel(Group(left_top, left_bottom), box=box.SIMPLE)

    def get_main_middle(self):
        data = self.scrapper.matches

        next_matches = data["matches"][:6]
        items = []
        for each in next_matches:
            matches = Table.grid(expand=True)
            matches.add_column()
            matches.add_column(justify="center")
            matches.add_column()

            matches.add_row("", each["competition"]["label"], "")
            matches.add_row("", datetime.fromtimestamp(each["match"]["time"]).strftime("%d.%m.%Y %A - %H:%M"), "")
            matches.add_row(
                Align.left(data["teams"][str(each["match"]["home"])]["name"]),
                each["match"]["result"],
                Align.right(data["teams"][str(each["match"]["away"])]["name"]),
            )
            items.append(Panel(matches, padding=(0, 3), box=box.HORIZONTALS))

        return Panel(
            Panel(
                Group(*items),
                title="[cyan][b]SONRAKİ KARŞILAŞMALAR[/b][/cyan]"
            ),
            box=box.SIMPLE
        )

    def get_main_right(self):
        items = []
        for each in self.scrapper.rumors[:4]:
            rumors = Table.grid(expand=True)
            rumors.add_column()
            rumors.add_column(justify="center")
            rumors.add_column()
            rumors.add_row("", each["player"]["name"], "", style="bold")
            rumors.add_row("Yaş", ": ", str(each["player"]["age"]))
            rumors.add_row("Mevki", ": ", each["player"]["position"])
            rumors.add_row("Piyasa değeri", ": ", each["player"]["marketValue"])
            rumors.add_row(each["team1"]["name"], ">> ", each["team2"]["name"], style="bold italic")
            items.append(Panel(rumors, padding=(0, 3), box=box.HORIZONTALS), )
        return Panel(
            Panel(
                Group(*items),
                title="[cyan][b]GÜNCEL SÖYLENTİLER[/b][/cyan]"
            ),
            box=box.SIMPLE
        )

    @staticmethod
    def get_footer():
        table = Table.grid(expand=True)
        table.add_column()
        table.add_column()
        table.add_column()
        table.add_row("quit", ": ", "CTRL + C")
        table.add_row("credit", ": ", Text("@osmanuygar", style="link https://github.com/osmanuygar"))
        return Panel(table, box=box.HORIZONTALS)


class Footballers:
    def __init__(self):
        self.scrapper = Scraper()
        self.layout = Layout(name="root")
        self.layout.split(
            Layout(name="main", ratio=24),
            Layout(name="footer", ratio=2),
        )

    def setup(self):
        self.layout["main"].update(self.get_main())
        self.layout["footer"].update(self.get_footer())

    def run(self):
        with Live(self.layout, screen=True):
            while True:
                sleep(1)

    @staticmethod
    def get_footer():
        table = Table.grid(expand=True)
        table.add_column()
        table.add_column()
        table.add_column()
        table.add_row("quit", ": ", "CTRL + C")
        table.add_row("credit", ": ", Text("@osmanuygar", style="link https://github.com/osmanuygar"))
        return Panel(table, box=box.HORIZONTALS)

    def get_main(self):
        standings = Table(expand=True)
        standings.add_column(header="Player")
        standings.add_column(header="Age")
        standings.add_column(header="Position")
        standings.add_column(header="Market Value")

        for i in range(0, len(self.scrapper.players["Player"]),1):
            standings.add_row(self.scrapper.players["Player"][i], self.scrapper.players["Age"][i]
                              , self.scrapper.players["Position"][i],self.scrapper.players["Market Value"][i])
        return Panel(standings, title="[cyan][b]Besiktas Squad[/b][/cyan]", box=box.SQUARE)


class Stats:
    def __init__(self):
        self.scrapper = Scraper()
        self.layout = Layout(name="root")
        self.layout.split(
            Layout(name="main", ratio=10),
            Layout(name="footer", ratio=2),
        )
        self.layout["main"].split_row(
            Layout(name="main-left", ratio=1),
            Layout(name="main-right", ratio=1)
        )

    def setup(self):
        self.layout["main-left"].update(self.get_main_left_stats())
        self.layout["main-right"].update(self.get_main_right_stats())
        self.layout["footer"].update(self.get_footer())

    def run(self):
        with Live(self.layout, screen=True):
            while True:
                sleep(1)

    def get_main_left_stats(self):
        standings = Table(expand=True)
        standings.add_column(header="Player")
        standings.add_column(header="Position")
        standings.add_column(header="Goals")

        for i in range(0, len(self.scrapper.goals["Player"]), 1):
            standings.add_row(self.scrapper.goals["Player"][i],  self.scrapper.goals["Position"][i], self.scrapper.goals["Goals"][i])
        return Panel(standings, title="[cyan][b]TOP GOALSCORERS[/b][/cyan]", box=box.SQUARE)

    def get_main_right_stats(self):
        standings = Table(expand=True)
        standings.add_column(header="Player")
        standings.add_column(header="Position")
        standings.add_column(header="Assists")

        for i in range(0, len(self.scrapper.assists["Player"]), 1):
            standings.add_row(self.scrapper.assists["Player"][i], self.scrapper.assists["Position"][i],
                              self.scrapper.assists["Assists"][i])
        return Panel(standings, title="[cyan][b]MOST ASSISTS[/b][/cyan]", box=box.SQUARE)


    def get_footer(self):
        table = Table.grid(expand=True)
        table.add_column()
        table.add_column()
        table.add_column()
        table.add_row("quit", ": ", "CTRL + C")
        table.add_row("credit", ": ", Text("@osmanuygar", style="link https://github.com/osmanuygar"))
        return Panel(table, box=box.HORIZONTALS)
