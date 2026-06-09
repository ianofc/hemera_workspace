import { describe, it, expect, beforeEach, vi } from "vitest";
import { moodleService, MoodleConfig } from "../services/moodleService";

describe("moodleService Tests", () => {
  beforeEach(() => {
    localStorage.clear();
    vi.restoreAllMocks();
  });

  it("should retrieve default config if none is saved", () => {
    const config = moodleService.getConfig();
    expect(config.url).toBe("https://moodle.hemera.edu.br");
    expect(config.token).toBe("");
    expect(config.autoSync).toBe(true);
  });

  it("should save and retrieve custom moodle config", () => {
    const customConfig: MoodleConfig = {
      url: "https://moodle.custom.edu.br",
      token: "secret-token-123",
      autoSync: false
    };
    moodleService.saveConfig(customConfig);

    const config = moodleService.getConfig();
    expect(config).toEqual(customConfig);
  });

  it("should return default events and grades lists", () => {
    const events = moodleService.getSyncedEvents();
    expect(events.length).toBeGreaterThan(0);
    expect(events[0].id).toBe("m-1");

    const grades = moodleService.getSyncedGrades();
    expect(grades.length).toBeGreaterThan(0);
    expect(grades[0].id).toBe("g-1");
  });

  it("should simulate Moodle sync and update status if token is provided", async () => {
    const config: MoodleConfig = {
      url: "https://moodle.hemera.edu.br",
      token: "valid-user-token",
      autoSync: true
    };

    const res = await moodleService.syncMoodle(config);
    expect(res.success).toBe(true);

    // Deve ter modificado o status do evento 'm-1' de pending para submitted
    const events = moodleService.getSyncedEvents();
    const event1 = events.find(ev => ev.id === "m-1");
    expect(event1?.status).toBe("submitted");

    // Deve ter adicionado a nota 'g-3'
    const grades = moodleService.getSyncedGrades();
    const grade3 = grades.find(g => g.id === "g-3");
    expect(grade3).toBeDefined();
    expect(grade3?.grade).toBe(9.0);
  });
});
