import flet as ft
import asyncio

class Countdown(ft.Text):
    def __init__(self, seconds, label):
        super().__init__()
        self.original_seconds = seconds
        self.seconds = seconds
        self.label = label
        self.running = False
        self.size = 48
        self.value = self.format_time()

    def format_time(self):
        mins, secs = divmod(self.seconds, 60)
        return f"{mins:02d}:{secs:02d}"

    def did_mount(self):
        self.running = True
        self.page.run_task(self.update_timer)

    def will_unmount(self):
        self.running = False

    async def update_timer(self):
        while self.running:
            while self.seconds > 0 and self.running:
                await asyncio.sleep(1)
                self.seconds -= 1
                self.value = self.format_time()
                self.update()
            
            if self.seconds <= 0:
                self.value = "00:00"
                self.update()
                break

    def reset(self):
        self.seconds = self.original_seconds
        self.value = self.format_time()
        self.update()

def main(page: ft.Page):
    timers = {
        "1_min": Countdown(60, "1 min"),
        "1,5_min": Countdown(90, "1,5 min"),
        "2_min": Countdown(120, "2 min"),
    }

    content = ft.Column(
        controls=[
            ft.Text("Select a timer", size=20)
        ],
        expand=True
    )

    def handle_dismissal(e):
        print("Drawer dismissed!")

    def handle_change(e):
        selected_index = e.control.selected_index
        print(f"Selected Index changed: {selected_index}")
        content.controls.clear()
        
        if selected_index == 0:
            timer = timers["1_min"]
            content.controls.append(ft.Text("1 min", size=24))
            content.controls.append(timer)
            content.controls.append(
                ft.Row([
                    ft.ElevatedButton(
                        "Start", 
                        on_click=lambda e: start_timer(timers["1_min"])
                    ),
                    ft.ElevatedButton(
                        "Pause", 
                        on_click=lambda e: pause_timer(timers["1_min"])
                    ),
                    ft.ElevatedButton(
                        "Reset Timer", 
                        on_click=lambda e: timers["1_min"].reset()
                    )
                ])
            )
            
        elif selected_index == 1:
            timer = timers["1,5_min"]
            content.controls.append(ft.Text("1,5 min", size=24))
            content.controls.append(timer)
            content.controls.append(
                ft.Row([
                    ft.ElevatedButton(
                        "Start", 
                        on_click=lambda e: start_timer(timers["1,5_min"])
                    ),
                    ft.ElevatedButton(
                        "Pause", 
                        on_click=lambda e: pause_timer(timers["1,5_min"])
                    ),
                    ft.ElevatedButton(
                        "Reset Timer", 
                        on_click=lambda e: timers["1,5_min"].reset()
                    )
                ])
            )
            
        elif selected_index == 2:
            timer = timers["2_min"]
            content.controls.append(ft.Text("2 min", size=24))
            content.controls.append(timer)
            content.controls.append(
                ft.Row([
                    ft.ElevatedButton(
                        "Start", 
                        on_click=lambda e: start_timer(timers["2_min"])
                    ),
                    ft.ElevatedButton(
                        "Pause", 
                        on_click=lambda e: pause_timer(timers["2_min"])
                    ),
                    ft.ElevatedButton(
                        "Reset Timer", 
                        on_click=lambda e: timers["2_min"].reset()
                    )
                ])
            )
        
        content.update()
        page.close(drawer)

    def start_timer(timer):
        timer.running = True
        timer.page.run_task(timer.update_timer)

    def pause_timer(timer):
        timer.running = False

    drawer = ft.NavigationDrawer(
        on_dismiss=handle_dismissal,
        on_change=handle_change,
        controls=[
            ft.Container(height=12),
            ft.NavigationDrawerDestination(
                label="1 min",
                icon=ft.Icons.TIMER_OUTLINED,
                selected_icon=ft.Icons.TIMER,
            ),
            ft.Divider(thickness=2),
            ft.NavigationDrawerDestination(
                icon=ft.Icons.TIMER_OUTLINED,
                label="1,5 min",
                selected_icon=ft.Icons.TIMER,
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icons.TIMER_OUTLINED,
                label="2 min", 
                selected_icon=ft.Icons.TIMER,
            ),
        ],
    )
    
    page.add(
        ft.Column([
            ft.ElevatedButton("Timer Menu", on_click=lambda e: page.open(drawer)),
            content
        ], expand=True)
    )

ft.app(main)