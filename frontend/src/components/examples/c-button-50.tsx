import { Button } from "#components/ui/button"
import { ChevronLeftIcon } from "lucide-react"

export function Pattern() {
  return (
    <Button
      variant="link"
      className="group/back-button"
      render={<a href="#" />}
      nativeButton={false}
    >
      <ChevronLeftIcon data-icon="inline-start" aria-hidden="true" className="transition-transform duration-200 group-hover/back-button:-translate-x-1" />
      Go back
    </Button>
  )
}