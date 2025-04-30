**Wasteland Sweep** — динамичный top-down-шутер на Python + Pygame, где вы расчищаете опустевшие земли от бесчисленных угроз, шаг за шагом возвращая мир к жизни.

### Сюжет-затравка  
После грандиозного катаклизма мир превратился в бесплодные пустоши, кишащие мутантами, мародёрами и дикими машинами-охотниками. Вы — один из немногих механиков-рейнджеров, способных не только чинить свою броню и вооружение в полевых условиях, но и одним выстрелом разделывать целые отряды врагов. Отрядив ручного дрона-пылесоса, вы прочищаете каждую зону, собирая ценные ресурсы, охраняя караваны выживших и открывая новые безопасные маршруты сквозь руины прошлого мира.

### Ключевые особенности

| Геймплей                              | Технологии                                  |
|---------------------------------------|---------------------------------------------|
| **Полевая чистка.** После каждой зоны ваш дрон-сборщик увозит всё ценное: от запчастей до редких патронов. | **Python 3.12** + **Pygame 2.5** без внешних игровых движков. |
| **Модульное оружие.** Меняйте стволы, рукояти и прицельные модули прямо в бою, создавая гибридные пушки. | ECS-архитектура (Entity-Component-System) для лёгкого добавления новых компонентов. |
| **Опасные пыльные шторма.** Ветер и грязь затрудняют прицеливание, но открывают новые тактические возможности. | Горячая перезагрузка ассетов — меняйте спрайты и звуки без перезапуска игры. |
| **Система караванов.** Сопровождайте торговые караваны сквозь заражённые районы, получая награду за каждый доставленный груз. | Встроенный редактор карт и тайлов в dev-режиме. |
| **Кооператив до двух игроков.** Помогайте друг другу очищать пустоши, делясь ресурсами и устраивая совместные рейды. | Unit-тесты и GitHub Actions для CI/CD. |

### Почему «Wasteland Sweep»?  
*Wasteland* — безжизненная пустошь после катастрофы; *Sweep* — «прочистка» территории от угроз. Вместе они отражают суть вашей миссии: пройти по опустевшим землям и очистить их от опасностей.

### Чего ждать в ближайших релизах
- 🚚 **Улучшенный дрон-аспиратор**: новые модули для поиска и извлечения редких ресурсов.  
- 🏜️ **Новые биомы**: радиоактивные каньоны, обугленные леса и затопленные руины.  
- 💥 **Боссы-механизмы**: гигантские воркшопы-титаны, охраняющие стратегические точки.  
- 🎵 **Адаптивный саундтрек**: музыка меняется от тихого гудения дрели до сурового маршевого бита в разгар битвы.  

### Запуск проекта
```bash
git clone https://github.com/your-username/wasteland-sweep.git
cd wasteland-sweep
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run_game.py
```
---
**Wasteland Sweep** is a fast-paced top-down shooter built with Python + Pygame, where you clear barren wastelands of endless threats, restoring life to the world one zone at a time.

### Story Hook  
After a cataclysmic event, the world has become desolate wastelands teeming with mutants, raiders, and wild hunter-machines. You are one of the few mechanic-rangers capable of field-repairing your armor and weapons—and with a single shot, taking down entire enemy squads. Deploying your trusty vacuum-drone, you sweep through each area, salvaging valuable resources, escorting survivor caravans, and unlocking safe passageways through the ruins of the old world.

### Key Features

| Gameplay                              | Technology                                 |
|---------------------------------------|--------------------------------------------|
| **Field Sweep.** After each mission zone, your collection drone hauls away everything valuable—from spare parts to rare ammo. | **Python 3.12** + **Pygame 2.5**, no external game engines. |
| **Modular Weapons.** Swap barrels, grips, and targeting modules on the fly to create hybrid firearms. | ECS (Entity-Component-System) architecture for easy content expansion. |
| **Hazardous Dust Storms.** Wind and grit impair your aim but open new tactical opportunities. | Hot asset reloading—update sprites and sounds without restarting the game. |
| **Caravan System.** Escort trading caravans through infested areas to earn rewards for each delivered load. | Built-in map and tile editor in dev mode. |
| **Two-Player Co-op.** Team up to clear wastelands together, share resources, and coordinate joint raids. | Unit tests and GitHub Actions for CI/CD. |

### Why “Wasteland Sweep”?  
*Wasteland* signifies the dead, post-apocalyptic terrain; *Sweep* means clearing it of dangers. Together, they capture the essence of your mission: to traverse the empty lands and cleanse them of threats.

### Coming Soon
- 🚚 **Upgraded Vacuum Drone:** New modules for locating and extracting rare resources.  
- 🏜️ **New Biomes:** Radioactive canyons, charred forests, and submerged ruins.  
- 💥 **Mech Bosses:** Giant workshop titans guarding strategic strongholds.  
- 🎵 **Adaptive Soundtrack:** Music shifts from the faint hum of drills to a pounding march in the heat of battle.  

### Getting Started
```bash
git clone https://github.com/your-username/wasteland-sweep.git
cd wasteland-sweep
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run_game.py
```
