import random

# ─── Environment ──────────────────────────────────────────────────────────────
class VacuumEnvironment:
    """
    Represents the vacuum-cleaner world.
    Rooms are labelled A, B, C, … and can be 'Clean' or 'Dirty'.
    """
    def __init__(self, rooms):
        # Randomly assign dirt status to each room at the start
        self.rooms     = {room: random.choice(['Clean', 'Dirty']) for room in rooms}
        self.room_list = rooms   # Ordered list of room names

    def perceive(self, location):
        """Return the dirt status ('Clean' or 'Dirty') at the given location."""
        return self.rooms[location]

    def execute(self, location, action):
        """Apply the agent's chosen action to the environment."""
        if action == 'SUCK':
            self.rooms[location] = 'Clean'
            print(f"    ACTION : SUCK       → Room {location} is now Clean.")
        elif action == 'MOVE_RIGHT':
            print(f"    ACTION : MOVE_RIGHT → Leaving Room {location}.")
        elif action == 'MOVE_LEFT':
            print(f"    ACTION : MOVE_LEFT  → Returning to start from Room {location}.")

    def all_clean(self):
        """Return True only if every room is clean."""
        return all(status == 'Clean' for status in self.rooms.values())

    def display(self):
        """Print the current dirt status of all rooms."""
        status_str = '  '.join(f"{r}:[{s}]" for r, s in self.rooms.items())
        print(f"    Rooms  : {status_str}")


# ─── Agent ────────────────────────────────────────────────────────────────────
class VacuumAgent:
    """
    Simple reflex vacuum-cleaner agent.

    Percept : (current_location, dirt_status)
    Actions : SUCK | MOVE_RIGHT | MOVE_LEFT

    Strategy:
      - If the current room is Dirty → SUCK.
      - Otherwise move right to the next room.
      - When the last room is reached, move back left to the first room.
      - Repeat until all rooms are clean.

    Performance Measure:
      +10 points for each room cleaned (SUCK action on a dirty room).
      -1  point  for each step taken (movement cost).
    """
    def __init__(self, environment):
        self.env          = environment
        self.location_idx = 0    # Index into room_list; agent starts at first room
        self.performance  = 0    # Accumulated performance score
        self.steps        = 0    # Total steps taken

    @property
    def location(self):
        """Return the current room label."""
        return self.env.room_list[self.location_idx]

    def choose_action(self, dirt_status):
        """
        Rule-based action selection (simple reflex):
          Dirty → SUCK
          Clean → move to next room (or back to start from last room)
        """
        if dirt_status == 'Dirty':
            return 'SUCK'
        if self.location_idx < len(self.env.room_list) - 1:
            return 'MOVE_RIGHT'
        return 'MOVE_LEFT'   # At last room; cycle back to beginning

    def run(self, max_steps=100):
        """Run the agent until all rooms are clean or the step limit is hit."""
        print("\n" + "=" * 55)
        print("       VACUUM CLEANER AGENT — SIMULATION START")
        print("=" * 55)
        print(f"\nRooms in environment : {self.env.room_list}")
        print("Initial dirt status  :")
        self.env.display()
        print()

        while not self.env.all_clean() and self.steps < max_steps:
            self.steps   += 1
            loc           = self.location
            dirt_status   = self.env.perceive(loc)

            print(f"  Step {self.steps:02d} | Room: {loc} | Status: {dirt_status}")

            action = self.choose_action(dirt_status)
            self.env.execute(loc, action)

            # ── Update performance score ────────────────────────────────
            if action == 'SUCK':
                self.performance += 10   # Reward for cleaning
            self.performance -= 1        # Cost per step

            # ── Update agent's position ─────────────────────────────────
            if action == 'MOVE_RIGHT':
                self.location_idx += 1
            elif action == 'MOVE_LEFT':
                self.location_idx = 0    # Reset to first room

            self.env.display()
            print()

        # ── Final report ────────────────────────────────────────────────
        print("=" * 55)
        print("               SIMULATION COMPLETE")
        print("=" * 55)
        print("\nFinal room status:")
        self.env.display()
        print()

        if self.env.all_clean():
            print(f"  ✔ All rooms cleaned in {self.steps} step(s).")
        else:
            print(f"  ✘ Max steps ({max_steps}) reached. Some rooms still dirty.")

        print(f"  Performance Score : {self.performance}")
        print("=" * 55 + "\n")


# ─── Main ─────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    random.seed(42)   # Fix seed so results are reproducible

    # Define the rooms in the environment (extend this list to add more rooms)
    rooms = ['A', 'B', 'C', 'D']

    env   = VacuumEnvironment(rooms)
    agent = VacuumAgent(env)
    agent.run()