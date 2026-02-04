import { Connection, Repository, FindManyOptions } from 'typeorm';
import { AuditEntry, AuditAction } from '../models/audit-entry';

export interface AuditFilter {
  userId?: string;
  taskId?: string;
  dateFrom?: Date;
  dateTo?: Date;
  action?: AuditAction;
}

export class AuditQueryService {
  private auditRepository: Repository<AuditEntry>;

  constructor(private connection: Connection) {
    this.auditRepository = this.connection.getRepository(AuditEntry);
  }

  /**
   * Get audit entries for a specific task ID
   * @param taskId The task ID to query audits for
   * @returns Array of audit entries
   */
  async getAuditsByTaskId(taskId: string): Promise<AuditEntry[]> {
    const options: FindManyOptions<AuditEntry> = {
      where: { taskId },
      order: { createdAt: 'ASC' }
    };

    return await this.auditRepository.find(options);
  }

  /**
   * Get audit entries by various filters
   * @param filter Filter options
   * @returns Array of audit entries
   */
  async getAuditsByFilter(filter: AuditFilter): Promise<AuditEntry[]> {
    const options: FindManyOptions<AuditEntry> = {
      where: {
        ...(filter.userId && { userId: filter.userId }),
        ...(filter.taskId && { taskId: filter.taskId }),
        ...(filter.action && { action: filter.action }),
        ...(filter.dateFrom && { createdAt: { $gte: filter.dateFrom } }),
        ...(filter.dateTo && { createdAt: { $lte: filter.dateTo } })
      },
      order: { createdAt: 'DESC' }
    };

    // Note: TypeORM uses different syntax for date comparisons
    if (filter.dateFrom || filter.dateTo) {
      options.where = {
        ...options.where,
      };

      if (filter.dateFrom && filter.dateTo) {
        (options.where as any).createdAt = {
          $between: [filter.dateFrom, filter.dateTo]
        };
      } else if (filter.dateFrom) {
        (options.where as any).createdAt = {
          $gte: filter.dateFrom
        };
      } else if (filter.dateTo) {
        (options.where as any).createdAt = {
          $lte: filter.dateTo
        };
      }
    }

    return await this.auditRepository.find(options);
  }

  /**
   * Get audit entries by user ID
   * @param userId The user ID to query audits for
   * @returns Array of audit entries
   */
  async getAuditsByUserId(userId: string): Promise<AuditEntry[]> {
    const options: FindManyOptions<AuditEntry> = {
      where: { userId },
      order: { createdAt: 'DESC' }
    };

    return await this.auditRepository.find(options);
  }

  /**
   * Get all audit entries
   * @returns Array of all audit entries
   */
  async getAllAudits(): Promise<AuditEntry[]> {
    const options: FindManyOptions<AuditEntry> = {
      order: { createdAt: 'DESC' }
    };

    return await this.auditRepository.find(options);
  }
}