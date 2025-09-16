import pygame
import constants
import neat
import os
import sys
import random
import pickle
from objects.defaultbird import DefaultBird
from utils.base_object import BaseObject
from objects.pipe import Pipe
from objects.floor import Floor
from objects.score import Score
from utils.movement import Movement
from utils.race_stats import RaceStats

generation = 0
hi_score = 0
hi_score_bird = None


def eval_genomes(genomes, config):
    global generation
    global hi_score
    global hi_score_bird
    generation += 1
    pygame.init()
    game_display = pygame.display.set_mode((constants.DISPLAY_WIDTH, constants.DISPLAY_HEIGHT))
    pygame.display.set_caption("AI Flappy Bird")
    pygame.display.set_icon(pygame.image.load(constants.ICON_PATH))
    clock = pygame.time.Clock()
    running = True

    if constants.CURRENT_MODE == constants.AUTO_RACE_MODE:
        constants.FPS = float('inf')

    pipe_image = pygame.image.load(constants.PIPE_IMAGE_PATH)
    primary_pipes = Pipe(constants.PIPE_WIDTH, constants.PIPE_GAP_HEIGHT, game_display, pipe_image)
    secondary_pipes = Pipe(constants.PIPE_WIDTH, constants.PIPE_GAP_HEIGHT, game_display, pipe_image)
    secondary_pipes.set_x(int((constants.DISPLAY_WIDTH * 1.5) + (constants.PIPE_WIDTH / 2)))

    floor = Floor(constants.DISPLAY_HEIGHT - constants.FLOOR_HEIGHT, constants.FLOOR_HEIGHT, game_display,
                  pygame.image.load(constants.FLOOR_IMAGE_PATH))

    players = []

    ge = []
    nets = []

    used_ids = []
    for genome_id, genome in genomes:
        bird_id = random.randint(1,99)
        while bird_id in used_ids:
            bird_id = random.randint(1, 99)
        used_ids.append(bird_id)
        players.append(DefaultBird(game_display, bird_id))
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    bird_stats = RaceStats("data/race_stats.json")

    bird_id_font = pygame.font.Font("assets/font/sen-extrabold.otf", 20)
    bird_stats_font = pygame.font.Font("assets/font/sen-bold.otf", 15)

    # show players before race
    start_race = False
    if constants.CURRENT_MODE == constants.AUTO_RACE_MODE or constants.CURRENT_MODE == constants.TRAINING_MODE:
        start_race = True
    while not start_race:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # start race
                    start_race = True

        game_display.fill(constants.BG_COLOR)

        banner_text = (pygame.font.Font("assets/font/sen-extrabold.otf", 50).
                       render("Competitors", True, constants.SCORE_COLOR))
        game_display.blit(banner_text, (constants.DISPLAY_WIDTH // 2 - banner_text.get_width() // 2, 20))

        offset = 20
        increment = (constants.DISPLAY_WIDTH - offset) // len(players)
        for player in players:
            player.set_x(offset)
            offset += increment
            player.set_y(constants.DISPLAY_HEIGHT // 2)
            player.draw()

            bird_id_text = f"{'0' + str(player.bird_id) if player.bird_id < 10 else player.bird_id}"
            bird_id_text = bird_id_font.render(bird_id_text, True, constants.SCORE_COLOR)
            game_display.blit(bird_id_text, (player.x + player.width // 2 - 10, player.y + player.height +
                              bird_id_text.get_height() // 2))

            bird_stats_text = ["Average", f"Score: {bird_stats.get_average_score(str(player.bird_id))}", "",
                               f"Win rate:", f"{bird_stats.get_win_percentage(str(player.bird_id)):.1f}%"]
            label = []
            for i, text in enumerate(bird_stats_text):
                label.append(bird_stats_font.render(text, True, constants.SCORE_COLOR))
                game_display.blit(label[i], (player.x + player.width // 2 - label[i].get_width() // 2,
                                             player.y + player.height + bird_id_text.get_height() + 10 + i * 20))
            # bird_stats_text = bird_stats_font.render(bird_stats_text, True, constants.SCORE_COLOR)
            # game_display.blit(bird_stats_text, (player.x + player.width // 2 - bird_stats_text.get_width() // 2,
            #                                     player.y + player.height + bird_id_text.get_height() + 10))

        pygame.display.update()

    # reset players for race
    for player in players:
        player.reset()

    score = Score(constants.DISPLAY_WIDTH // 2, 20,
                  pygame.font.Font(*constants.SCORE_FONT), constants.SCORE_COLOR, game_display)

    neat_score = 0

    primary_pipes.link_score(score)
    secondary_pipes.link_score(score)

    losers = []
    losers_scores = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    if constants.CURRENT_MODE == constants.DEBUG_MODE:
                        DefaultBird.kill_random()

        if len(players) == 0:
            break

        # kill random bird
        if random.randint(0, 100) == 0:
            DefaultBird.kill_random()

        neat_score += 1

        game_display.fill(constants.BG_COLOR)

        for loser in losers:
            loser.kill_self = False
            if loser.get_x() < -loser.get_width():
                if loser in BaseObject.child:
                    BaseObject.child.remove(loser)

        BaseObject.update_all()

        # draw eliminated
        eliminated_birds = False
        loser_x_pos = constants.DISPLAY_WIDTH - 20
        for loser in losers:
            if loser in BaseObject.child:
                continue
            loser.set_movement(Movement(0, 0))
            loser.images.reset()
            loser.set_x(loser_x_pos - loser.get_width())
            loser.set_y(loser.get_height() + 20)
            loser.draw()
            loser_x_pos -= loser.get_width() + 20
            eliminated_birds = True
        if eliminated_birds:
            eliminated_text = (pygame.font.Font("freesansbold.ttf", 30).
                               render("Eliminated", True, constants.SCORE_COLOR))
            game_display.blit(eliminated_text, (constants.DISPLAY_WIDTH - 170, 20))

        for i, player in enumerate(players):
            if floor.check_collision(player) \
                    or primary_pipes.check_collision(player) \
                    or secondary_pipes.check_collision(player):
                players.remove(player)
                player.set_movement(Movement(-5, 0))
                losers.append(player)
                losers_scores.append(neat_score)
                ge[i].fitness += neat_score / 10
                genome = ge.pop(i)
                nets.pop(i)
            else:
                # check which pipe set is closer
                primary_pipe_distance = primary_pipes.get_gap().x - player.x
                secondary_pipe_distance = secondary_pipes.get_gap().x - player.x
                if primary_pipe_distance < -primary_pipes.get_gap().width:
                    primary_pipe_distance = 999999999
                if secondary_pipe_distance < -secondary_pipes.get_gap().width:
                    secondary_pipe_distance = 999999999
                if primary_pipe_distance < secondary_pipe_distance:
                    pipe_midpoint = primary_pipes.get_gap().y + primary_pipes.get_gap().height // 2
                    dist_to_center = abs(player.y - pipe_midpoint)
                    ge[i].fitness += (1 - dist_to_center / 100)
                else:
                    pipe_midpoint = secondary_pipes.get_gap().y + secondary_pipes.get_gap().height // 2
                    dist_to_center = abs(player.y - pipe_midpoint)
                    ge[i].fitness += (1 - dist_to_center / 100)

        for i, player in enumerate(players):
            if player.kill_self:
                continue
            pipes_1 = primary_pipes.get_gap()
            pipes_2 = secondary_pipes.get_gap()
            pipes_1_distance = pipes_1.x - player.x
            pipes_2_distance = pipes_2.x - player.x
            if pipes_1_distance < -pipes_1.width:
                pipes_1_distance = 999999999
            if pipes_2_distance < -pipes_2.width:
                pipes_2_distance = 999999999
            closest_pipe = pipes_1 if pipes_1_distance < pipes_2_distance else pipes_2
            output = nets[i].activate((
                player.y,
                player.x - closest_pipe.x,
                player.y - (closest_pipe.y + closest_pipe.height // 2)
            ))
            if output[0] > 0.5:
                player.jump()

        pygame.display.update()
        clock.tick(constants.FPS)

    # Show winners
    losers = losers[::-1]

    stats_updated = False
    advance = False
    if constants.CURRENT_MODE == constants.AUTO_RACE_MODE or constants.CURRENT_MODE == constants.TRAINING_MODE:
        advance = True
    while not advance:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # advance to next generation
                    advance = True

        game_display.fill(constants.BG_COLOR)
        offset = 20
        increment = (constants.DISPLAY_WIDTH - offset) // len(losers)
        for i, player in enumerate(losers):
            player.set_movement(Movement(0, 0))
            player.images.reset()
            player.set_x(offset)
            offset += increment
            player.set_y(constants.DISPLAY_HEIGHT // 2)
            player.draw()

            placement_drawing = None
            if i == 0:
                placement_drawing = pygame.image.load(constants.FIRST_PLACE_IMAGE_PATH)
            elif i == 1:
                placement_drawing = pygame.image.load(constants.SECOND_PLACE_IMAGE_PATH)
            elif i == 2:
                placement_drawing = pygame.image.load(constants.THIRD_PLACE_IMAGE_PATH)

            if placement_drawing is not None:
                placement_drawing = pygame.transform.scale(placement_drawing,
                                                           (constants.PLACEMENT_WIDTH, constants.PLACEMENT_HEIGHT))
                game_display.blit(placement_drawing, (player.x + player.width // 2 - placement_drawing.get_width() // 2,
                                                      player.y - placement_drawing.get_height() - 10))

            bird_id_text = f"{'0' + str(player.bird_id) if player.bird_id < 10 else player.bird_id}"
            bird_id_text = bird_id_font.render(bird_id_text, True, constants.SCORE_COLOR)
            game_display.blit(bird_id_text, (player.x + player.width // 2 - 10, player.y + player.height +
                                             bird_id_text.get_height() // 2))

        pygame.display.update()

        # update stats
        if stats_updated is False:
            bird_stats.add_race([str(player.bird_id) for player in losers[::-1]], losers_scores)
            stats_updated = True

    BaseObject.clear_all()


def run(config_filepath):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_filepath
    )
    pop = neat.Population(config)
    pop.run(eval_genomes, 50)


def replay():
    try:
        pop = load_population()
        pop.run(eval_genomes, 1)
    except FileNotFoundError:
        print("No data found. Please train the AI first.")
        sys.exit(0)


def train(config_filepath):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_filepath
    )

    pop = neat.Population(config)

    # check if old data exists
    if os.path.exists("data/genomes"):
        if len(os.listdir("data/genomes")) > 0:
            print("Old data found. Do you want to continue training? (y/n)")
            response = input()
            if response.lower() == "n":
                return
            pop = load_population()
    else:
        os.makedirs("data/genomes")

    pop.run(eval_genomes, 10)

    save_population(pop)


def save_population(population: neat.Population):
    with open(f"data/genomes/population.pkl", "wb") as f:
        pickle.dump(population, f)


def load_population() -> neat.Population:
    with open(f"data/genomes/population.pkl", "rb") as f:
        return pickle.load(f)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    if constants.CURRENT_MODE == constants.TRAINING_MODE:
        train(config_path)
    else:
        while True:
            replay()
