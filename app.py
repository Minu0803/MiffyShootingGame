import pygame
import random
import math

# Pygame 초기화
pygame.init()

# 화면 크기 설정
screen_width = 1500
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))

# 게임 제목 및 아이콘 설정
pygame.display.set_caption("Space Shooter")
icon = pygame.image.load('spaceship.png')  # 아이콘 이미지 파일을 프로젝트 디렉토리에 배치해야 합니다
pygame.display.set_icon(icon)

# 배경 이미지
background = pygame.image.load('space.png')  # 배경 이미지 파일

# 플레이어
player_img = pygame.image.load('miffy.png')  # 플레이어 우주선 이미지
player_x = 370
player_y = 480
player_x_change = 0
player_y_change = 0  # 상하 이동을 위한 변수 추가

# 적 이미지 크기
enemy_width = 64  # 적 이미지의 너비
enemy_height = 64  # 적 이미지의 높이

# 적 설정 함수
def create_enemies(num_of_enemies, level):
    enemy_img = []
    enemy_x = []
    enemy_y = []
    enemy_x_change = []
    enemy_y_change = []
    enemy_hp = []

    for i in range(num_of_enemies):
        enemy_img.append(pygame.image.load('enemy.png'))  # 적 이미지
        enemy_x.append(random.randint(0, screen_width - 64))
        enemy_y.append(random.randint(50, 150))
        enemy_x_change.append(2 + level)  # 레벨에 따라 속도 증가
        enemy_y_change.append(15)
        enemy_hp.append(3 + level)  # 레벨에 따라 HP 증가

    return enemy_img, enemy_x, enemy_y, enemy_x_change, enemy_y_change, enemy_hp

# 처음 적들 생성
level = 1
num_of_enemies = 6
enemy_img, enemy_x, enemy_y, enemy_x_change, enemy_y_change, enemy_hp = create_enemies(num_of_enemies, level)

# 총알
bullet_img = pygame.image.load('bullet.png')  # 총알 이미지
bullet_x = 0
bullet_y = player_y
bullet_x_change = 0
bullet_y_change = 20
bullet_state = "ready"  # "ready"는 화면에 없는 상태, "fire"는 발사 상태

# 점수
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

# 게임 오버 텍스트
over_font = pygame.font.Font('freesansbold.ttf', 64)

# 적 HP 표시용 폰트
hp_font = pygame.font.Font('freesansbold.ttf', 24)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def show_level(x, y):
    level_text = font.render("Level : " + str(level), True, (255, 255, 255))
    screen.blit(level_text, (x, y + 40))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def show_enemy_hp(x, y, hp):
    hp_text = hp_font.render(f"HP: {hp}", True, (255, 0, 0))  # 적의 HP를 빨간색으로 표시
    screen.blit(hp_text, (x, y - 20))  # 적의 HP를 적 바로 위에 표시


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))


# 적과 총알의 충돌을 감지하는 함수
def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    if (bullet_x >= enemy_x and bullet_x <= enemy_x + enemy_width and
        bullet_y >= enemy_y and bullet_y <= enemy_y + enemy_height):
        return True
    return False

# 게임 루프
running = True
while running:

    # 배경 화면 설정
    screen.fill((0, 0, 0))  # 검정색 화
    screen.blit(background, (0, 0))  # 배경 이미지

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 키보드 입력
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -8
            if event.key == pygame.K_RIGHT:
                player_x_change = 8
            if event.key == pygame.K_UP:
                player_y_change = -8
            if event.key == pygame.K_DOWN:
                player_y_change = 8
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player_y_change = 0

    # 플레이어 이동
    player_x += player_x_change
    player_y += player_y_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= screen_width - 64:
        player_x = screen_width - 64
    if player_y <= 0:
        player_y = 0
    elif player_y >= screen_height - 64:
        player_y = screen_height - 64

    # 적 이동 및 삭제할 적 관리
    enemies_to_remove = []  # 삭제할 적 리스트
    for i in range(num_of_enemies):
        # 게임 오버
        if enemy_y[i] > 440:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            game_over_text()
            break

        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 4 + level  # 레벨에 따라 이동 속도 증가
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= screen_width - 64:
            enemy_x_change[i] = -4 - level  # 레벨에 따라 이동 속도 증가
            enemy_y[i] += enemy_y_change[i]

        # 충돌 감지
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            bullet_y = player_y
            bullet_state = "ready"
            enemy_hp[i] -= 1  # 적의 HP 감소
            if enemy_hp[i] <= 0:  # HP가 0이면 적 제거
                score_value += 1
                enemies_to_remove.append(i)  # 삭제할 적 리스트에 추가

        enemy(enemy_x[i], enemy_y[i], i)
        show_enemy_hp(enemy_x[i], enemy_y[i], enemy_hp[i])  # 적의 HP 표시

    # 적 리스트에서 HP가 0인 적 제거
    for index in sorted(enemies_to_remove, reverse=True):
        del enemy_img[index]
        del enemy_x[index]
        del enemy_y[index]
        del enemy_x_change[index]
        del enemy_y_change[index]
        del enemy_hp[index]
        num_of_enemies -= 1

    # 적이 모두 제거된 경우 리젠과 레벨업
    if num_of_enemies == 0:
        level += 1  # 적이 모두 제거되면 레벨이 올라감
        num_of_enemies = 6 + level  # 레벨에 따라 적 수 증가
        enemy_img, enemy_x, enemy_y, enemy_x_change, enemy_y_change, enemy_hp = create_enemies(num_of_enemies, level)

    # 총알 이동
    if bullet_y <= 0:  # 총알이 화면 위로 벗어났을 때
        bullet_y = player_y
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change  # 총알이 위로 날아가는 모션

    # 플레이어 호출
    player(player_x, player_y)

    # 점수 및 레벨 표시
    show_score(text_x, text_y)
    show_level(text_x, text_y)

    # 화면 업데이트
    pygame.display.update()