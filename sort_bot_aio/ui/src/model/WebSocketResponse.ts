import { z } from "zod"

export default z.object({ "image": z.string().describe("Base64 encoded image").optional(), "referenceImage": z.string().describe("Base64 encoded image of the empty belt that is used for detecting bricks").optional() })
