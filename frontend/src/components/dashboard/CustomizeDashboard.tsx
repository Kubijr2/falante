import { useState } from "react";

import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { useAuth } from "@/context/AuthContext";
import { ALL_WIDGET_IDS, WIDGET_LABELS, type WidgetId } from "@/types/analytics";

export function CustomizeDashboard() {
  const { user, updateDashboardWidgets } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const [selected, setSelected] = useState<WidgetId[]>(
    (user?.dashboard_widgets as WidgetId[]) ?? []
  );
  const [isSaving, setIsSaving] = useState(false);

  function toggle(widgetId: WidgetId) {
    setSelected((prev) =>
      prev.includes(widgetId) ? prev.filter((id) => id !== widgetId) : [...prev, widgetId]
    );
  }

  async function handleSave() {
    setIsSaving(true);
    try {
      await updateDashboardWidgets(selected);
      setIsOpen(false);
    } finally {
      setIsSaving(false);
    }
  }

  if (!isOpen) {
    return (
      <Button variant="secondary" onClick={() => setIsOpen(true)}>
        Customize dashboard
      </Button>
    );
  }

  return (
    <Card className="flex flex-col gap-3">
      <p className="font-display text-lg">Choose your charts</p>
      <p className="text-sm text-ink/60 dark:text-ink-dark/60">
        Pick which analytics widgets show up on your Dashboard. This is saved to your account —
        it's just yours.
      </p>
      <div className="flex flex-col gap-2">
        {ALL_WIDGET_IDS.map((widgetId) => (
          <label key={widgetId} className="flex items-center gap-2 text-sm">
            <input
              type="checkbox"
              checked={selected.includes(widgetId)}
              onChange={() => toggle(widgetId)}
              className="h-4 w-4"
            />
            {WIDGET_LABELS[widgetId]}
          </label>
        ))}
      </div>
      <div className="flex justify-end gap-2 pt-2">
        <Button variant="ghost" onClick={() => setIsOpen(false)}>
          Cancel
        </Button>
        <Button onClick={handleSave} disabled={isSaving}>
          {isSaving ? "Saving…" : "Save"}
        </Button>
      </div>
    </Card>
  );
}
