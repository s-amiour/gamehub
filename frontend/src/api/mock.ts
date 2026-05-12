import data from './mock-data.json'
import type { User, UserList, UserCreate } from './users'
import type { Game, GameList, GameCreate } from './games'

const delay = (ms = 300) => new Promise(res => setTimeout(res, ms))

export const mockUsersApi = {
  list: async (limit = 20, offset = 0): Promise<UserList> => {
    await delay()
    const items = data.users.items.slice(offset, offset + limit) as User[]
    return { items, total: data.users.total, limit, offset }
  },

  get: async (id: string): Promise<User> => {
    await delay()
    const user = data.users.items.find(u => u.id === id) as User | undefined
    if (!user) throw new Error('User not found')
    return user
  },

  create: async (body: UserCreate): Promise<User> => {
    await delay()
    return {
      id: crypto.randomUUID(),
      username: body.username,
      email: body.email,
      is_active: true,
      created_at: new Date().toISOString(),
    }
  },
}

export const mockGamesApi = {
  list: async (limit = 20, offset = 0): Promise<GameList> => {
    await delay()
    const items = data.games.items.slice(offset, offset + limit) as Game[]
    return { items, total: data.games.total, limit, offset }
  },

  get: async (id: string): Promise<Game> => {
    await delay()
    const game = data.games.items.find(g => g.id === id) as Game | undefined
    if (!game) throw new Error('Game not found')
    return game
  },

  search: async (q: string, limit = 20, offset = 0): Promise<GameList> => {
    await delay()
    const lower = q.toLowerCase()
    const all = data.games.items.filter(g =>
      g.title.toLowerCase().includes(lower)
    ) as Game[]
    return { items: all.slice(offset, offset + limit), total: all.length, limit, offset }
  },

  create: async (body: GameCreate): Promise<Game> => {
    await delay()
    return {
      id: crypto.randomUUID(),
      title: body.title,
      genre: body.genre,
      platform: body.platform,
      release_year: body.release_year ?? null,
      cover_url: body.cover_url ?? null,
      created_at: new Date().toISOString(),
    }
  },
}
