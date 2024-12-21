import { z } from "zod"

export default z.object({ "image": z.string().describe("Base64 encoded image").optional() })
