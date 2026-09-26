import { Button } from "#components/ui/button"
import { SendIcon } from "lucide-react"

export function Pattern() {
  return (
    <Button size="lg">
      Send Message
      <SendIcon aria-hidden="true" />
    </Button>
  )
}