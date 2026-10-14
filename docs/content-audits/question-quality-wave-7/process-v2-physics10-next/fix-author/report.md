# physics-seesaw-machine — адресный fix-cycle

- Baseline: 3b5bcbe1d7bb495c73aa5850e7dd5ba9fe4539c7; beforeHash d2f0c9be67c91eeff790c86e1dbe190d9ce7188d44b1b74e20d7a1ff0cd30e1f.
- Вердикт: FIX; меняются только answers[1].note, answers[2].note и source.verifiedAt.
- Проверен полный OpenStax §9.3 body из Git: 364089 байт, SHA-256 b3d5cebb8b1aae0261ac4c6785c94473ac4abd5cf638c02051d4be5b207d52f3. Исходные headers подтверждены: initial + 44 range responses.
- Typed locators и основания для всех шести field groups сохранены в candidate.json.
- Прочитаны вся карточка, frozen id/topic/order/difficulty/key, правильная справка как допфакт и актуальные соседние карточки.
- Проверки ограничены JSON/UTF-8, hashes и frozen-полями. Полные тесты, build и runtime не запускались.
- Дальше координатор применяет patch; назначенный GPT-6.1 Sol независимо проверяет точный CURRENT. Неразрешённый дефект остаётся HOLD.
